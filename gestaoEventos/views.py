from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# Importe seus models e serializers
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
    Rota: /api/participantes/ [cite: 86]
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Permite que qualquer um se cadastre (POST), mas só autenticados veem a lista
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class EventoViewSet(viewsets.ModelViewSet):
    """
    Endpoint principal de Eventos.
    Rota: /api/eventos/ [cite: 79]
    """
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    # Leitura é pública, mas criar/editar exige login 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Rota: /api/eventos/{id}/atividades/ [cite: 83]
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
    Rota: /api/atividades/ [cite: 90]
    """
    queryset = Atividade.objects.all()
    serializer_class = AtividadeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Rota: /api/atividades/{id}/responsavel/ [cite: 92]
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