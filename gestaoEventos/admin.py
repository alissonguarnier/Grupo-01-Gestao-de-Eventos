from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import Evento, Atividade, UserEventos, Perfil
from .utils import render_to_pdf # Importe sua função utilitária
from django.contrib import messages #exibir mensagens


# 1. Configuração do Admin de EVENTOS
@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_inicio', 'data_fim', 'local') # O que aparece na lista
    list_filter = ('local', 'data_inicio')                      # <--- FILTROS LATERAIS
    search_fields = ('nome', 'descricao')                       # Barra de pesquisa

    # 1. nome da função abaixo
    actions = ['gerar_pdf_eventos']

    # 2. A função da ação 
    @admin.action(description='Gerar Relatório PDF dos Selecionados')
    def gerar_pdf_eventos(self, request, queryset):
        from .utils import render_to_pdf  
        
        context = {
            'eventos': queryset,
            'titulo': 'Relatório de Eventos Selecionados'
        }
        return render_to_pdf('relatorios/relatorio_eventos.html', context)
    


# 2. Configuração do Admin de ATIVIDADES
@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'evento', 'tipo', 'horario_inicio', 'responsavel')
    list_filter = ('evento', 'tipo', 'responsavel')             # <--- FILTRA POR EVENTO OU TIPO
    search_fields = ('titulo',)

    # 1. nome da função abaixo
    actions = ['gerar_pdf_atividades']

    # 2. A função da ação
    @admin.action(description='Gerar Relatório PDF dos Selecionados')
    def gerar_pdf_atividades(self, request, queryset):
        from .utils import render_to_pdf  
        
        # 1. select_related: Carrega evento e responsável para não travar o banco no loop do PDF
        # 2. order_by: Garante que a lista saia em ordem cronológica
        atividades = queryset.select_related('evento', 'responsavel').order_by('horario_inicio')
        
        context = {
            'atividades': atividades, 
            'titulo': 'Relatório de Atividades Selecionadas'
        }
        
        return render_to_pdf('relatorios/relatorio_atividades.html', context)


# 3. Configuração do Admin de INSCRIÇÕES (UserEventos)
@admin.register(UserEventos)
class UserEventosAdmin(admin.ModelAdmin):
    list_display = ('user', 'evento', 'status', 'data_inscricao')
    list_filter = ('status', 'evento', 'data_inscricao')        
    search_fields = ('user__username', 'evento__nome')

        # 1. nome da função abaixo
    actions = ['gerar_pdf_inscricoes', 'gerar_certificados']

    # 2. A função da ação
    @admin.action(description='Gerar Relatório PDF dos Selecionados')
    def gerar_pdf_inscricoes(self, request, queryset):
        from .utils import render_to_pdf  
        
        context = {'inscricoes': queryset, 'titulo': 'Relatório de Inscrições'}
        return render_to_pdf('relatorios/relatorio_inscricoes.html', context)

    @admin.action(description='Gerar Certificados (Apenas Confirmados)')
    def gerar_certificados(self, request, queryset):
        # 1. Filtra apenas quem tem status 'C' (Confirmado)
        # Ajuste o 'C' se no seu model for outra letra
        inscricoes_validas = queryset.filter(status='C').select_related('user', 'evento')
        
        # 2. Verificação de segurança
        if not inscricoes_validas.exists():
            # Mostra um erro no topo da tela se ninguém for apto
            messages.error(request, "Nenhuma inscrição selecionada possui status 'Confirmado'.")
            return None
    
        # 3. Gera o PDF
        context = {
            'inscricoes': inscricoes_validas,
            'titulo': 'Certificado de Participação'
        }
        return render_to_pdf('relatorios/certificado.html', context)


# 4. Configuração do Admin de PERFIL (Opcional)
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo', 'celular')
    list_filter = ('tipo',)                                     # <--- FILTRA SE É PALESTRANTE/ALUNO
    search_fields = ('user__username', 'user__email')


   # 1. nome da função abaixo
    actions = ['gerar_pdf_perfil']

    # 2. A função da ação
    @admin.action(description='Gerar Relatório PDF dos Selecionados')
    def gerar_pdf_perfil(self, request, queryset):
        from .utils import render_to_pdf  
        
        # 1. Extrai apenas os IDs dos usuários ligados aos perfis selecionados
        user_ids = queryset.values_list('user_id', flat=True)

        # Busca os objetos User completos
        # Isso garante que o template receba "User" e não "Perfil"
        users = User.objects.filter(id__in=user_ids).prefetch_related(
            'perfil',
            'usereventos_set__evento',
            'atividades_responsavel'
        )

        # 3. Reutiliza o mesmo HTML
        context = {
            'participantes': users,  # A variável tem que chamar 'participantes' para bater com o HTML
            'titulo': 'Relatório de Perfis Selecionados'
        }
        
        return render_to_pdf('relatorios/relatorio_participantes.html', context)
    

# --- Ação para USUÁRIOS ---
@admin.action(description='Gerar PDF de Usuários (Detalhado)')
def gerar_pdf_usuarios(modeladmin, request, queryset):
    # Otimização: Traz Perfil, Inscrições (com evento) e Atividades Responsáveis
    users = queryset.select_related('perfil').prefetch_related(
        'perfil',
        'usereventos_set__evento',
        'atividades_responsavel'  
    )
    
    context = {
        'participantes': users, 
        'titulo': 'Relatório de Usuários Selecionados'
    }

    return render_to_pdf('relatorios/relatorio_participantes.html', context)

# --- Ação para GRUPOS ---
@admin.action(description='Gerar PDF de Grupos (Detalhado)')
def gerar_pdf_grupos(modeladmin, request, queryset):
    # Otimização: Carrega usuários, inscrições (e seus eventos) e atividades que o usuário é dono
    grupos = queryset.prefetch_related(
        'user_set',                           # Traz os usuários do grupo
        'user_set__usereventos_set__evento',  # Traz os eventos onde o usuário se inscreveu
        'user_set__atividades_responsavel'             # Traz as atividades onde o usuário é responsável
    )
    
    context = {
        'grupos': grupos, 
        'titulo': 'Relatório Detalhado de Grupos'
    }
    return render_to_pdf('relatorios/relatorio_grupos.html', context)


# Desregistra o admin original
admin.site.unregister(User)
admin.site.unregister(Group)

# Cria e Registra o novo Admin de USUÁRIOS
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    actions = [gerar_pdf_usuarios]

# Cria e Registra o novo Admin de GRUPOS
@admin.register(Group)
class CustomGroupAdmin(GroupAdmin):
    actions = [gerar_pdf_grupos]