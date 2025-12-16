from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
# para gerar o pdf:
from .utils import render_to_pdf
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Prefetch

# Importando models e serializers
from .models import Evento, Atividade, UserEventos, Perfil
from .serializers import (
    UserSerializer, 
    EventoSerializer, 
    AtividadeSerializer, 
    UserEventosSerializer,
    EventoDashboardSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    """
    Endpoint para gerenciar participantes (Users + Perfil).
    Rota: /api/participantes/ 
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Permite que qualquer um se cadastre (POST), mas só autenticados veem a lista
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class EventoViewSet(viewsets.ModelViewSet):
    """
    Endpoint principal de Eventos.
    Rota: /api/eventos/ 
    """
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    # Leitura é pública, mas criar/editar exige login 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filterset_fields = ['local', 'data_inicio']

    # Rota: /api/eventos/{id}/atividades/ 
    @action(detail=True, methods=['get'])
    def atividades(self, request, pk=None):
        """Lista apenas as atividades de um evento específico"""
        evento = self.get_object()
        atividades = Atividade.objects.filter(evento=evento)
        serializer = AtividadeSerializer(atividades, many=True)
        return Response(serializer.data)

    # Rota: /api/eventos/{id}/participantes/ 
    @action(detail=True, methods=['get', 'post'])
    def participantes(self, request, pk=None):
        """
        GET: Lista participantes do evento.
        POST: Inscreve o usuário logado no evento.
        """
        evento = self.get_object()

        if request.method == 'GET':
            # Retorna quem está inscrito
            inscricoes = UserEventos.objects.filter(evento=evento)
            serializer = UserEventosSerializer(inscricoes, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            # Inscreve o usuário logado (request.user)
            # Verifica se já está inscrito para evitar duplicidade
            if UserEventos.objects.filter(user=request.user, evento=evento).exists():
                return Response(
                    {"mensagem": "Você já está inscrito neste evento."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Cria a inscrição
            inscricao = UserEventos.objects.create(user=request.user, evento=evento)
            serializer = UserEventosSerializer(inscricao)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Rota: /api/eventos/{id}/dashboard/ 
    @action(detail=True, methods=['get'])
    def dashboard(self, request, pk=None):
        """Retorna uma visão completa do evento (Atividades + Participantes)"""
        evento = self.get_object()
        # Usa o serializer especial que criamos para trazer tudo junto
        serializer = EventoDashboardSerializer(evento)
        return Response(serializer.data)

class AtividadeViewSet(viewsets.ModelViewSet):
    """
    Endpoint para gerenciar Atividades.
    Rota: /api/atividades/ 
    """
    queryset = Atividade.objects.all()
    serializer_class = AtividadeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Rota: /api/atividades/{id}/responsavel/ 
    @action(detail=True, methods=['patch'])
    def responsavel(self, request, pk=None):
        """Define um responsável pela atividade via ID do usuário"""
        atividade = self.get_object()
        responsavel_id = request.data.get('responsavel_id')
        
        if not responsavel_id:
            return Response({"erro": "ID do responsável não fornecido."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, pk=responsavel_id)
        atividade.responsavel = user
        atividade.save()
        
        return Response({"mensagem": f"Responsável definido: {user.username}"})
    

# ------------------ Funções para criar o pdf ----------------

# Função auxiliar para verificar se é staff

# No início do arquivo views.py

def is_staff_check(user):
    # 1. Se não estiver logado, barra direto
    if not user.is_authenticated:
        return False
        
    # 2. Se for Superusuário (admin geral), LIBERA GERAL
    if user.is_superuser:
        return True

    # 3. Se for usuário comum, verifica se tem perfil e se é do tipo Staff ('O')
    if hasattr(user, 'perfil') and user.perfil.is_grupo_staff:
        return True
        
    return False

# Desativei para usar o SuperUser
'''def is_staff_check(user):
    return user.is_authenticated and hasattr(user, 'perfil') and user.perfil.is_grupo_staff'''

# 1. Relatório de Eventos
@user_passes_test(is_staff_check)
def relatorio_eventos(request):
    '''eventos = Evento.objects.all().order_by('data_inicio').prefetch_related(
        'atividade_set', 
        'usereventos_set__user'
    )'''
    eventos = Evento.objects.all().order_by('data_inicio')


    context = {'eventos': eventos, 'titulo': 'Relatório Geral de Eventos'}
    return render_to_pdf('relatorios/relatorio_eventos.html', context)

# 2. Relatório de Atividades
@user_passes_test(is_staff_check)
def relatorio_atividades(request):
    # Busca todas as atividades, já trazendo os dados relacionados para ser rápido
    atividades = Atividade.objects.all().select_related('evento', 'responsavel').order_by('horario_inicio')
    
    context = {
        'atividades': atividades, 
        'titulo': 'Relatório Geral de Atividades'
    }
    
    return render_to_pdf('relatorios/relatorio_atividades.html', context)

# 3. Relatório de Participantes
@user_passes_test(is_staff_check)
def relatorio_participantes(request):
    # Pega usuários que são participantes (P)
    # Prefetch para otimizar a busca das inscrições (usereventos) e responsabilidades (atividade_set)
    participantes = User.objects.filter(perfil__tipo='P').order_by('first_name').prefetch_related(
        'usereventos_set__evento'
    )

    context = {'participantes': participantes, 'titulo': 'Relatório de Participantes'}
    return render_to_pdf('relatorios/relatorio_participantes.html', context)

# 4. Relatório de Inscrições
@user_passes_test(is_staff_check)
def relatorio_inscricoes(request):
    inscricoes = UserEventos.objects.all().select_related('user', 'evento').order_by('-data_inscricao')

    context = {
        'inscricoes': inscricoes,
        'titulo': 'Relatório Geral de Inscrições'
    }

    # Reutiliza o mesmo HTML que criamos para a Action do Admin
    return render_to_pdf('relatorios/relatorio_inscricoes.html', context)

@user_passes_test(is_staff_check)
def relatorio_grupos_geral(request):
    # Busca TODOS os grupos com a otimização de consulta
    grupos = Group.objects.all().prefetch_related(
        'user_set',                           
        'user_set__usereventos_set__evento',  
        'user_set__atividades_responsavel'
    )
    
    context = {
        'grupos': grupos, 
        'titulo': 'Relatório Geral de Grupos'
    }
    # Reutiliza o mesmo HTML bonito que já criamos
    return render_to_pdf('relatorios/relatorio_grupos.html', context)