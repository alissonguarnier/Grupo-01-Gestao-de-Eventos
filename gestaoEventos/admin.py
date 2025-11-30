from django.contrib import admin
from .models import Evento, Atividade, UserEventos, Perfil

# 1. Configuração do Admin de EVENTOS
@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_inicio', 'data_fim', 'local') # O que aparece na lista
    list_filter = ('local', 'data_inicio')                      # <--- FILTROS LATERAIS
    search_fields = ('nome', 'descricao')                       # Barra de pesquisa

# 2. Configuração do Admin de ATIVIDADES
@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'evento', 'tipo', 'horario_inicio', 'responsavel')
    list_filter = ('evento', 'tipo', 'responsavel')             # <--- FILTRA POR EVENTO OU TIPO
    search_fields = ('titulo',)

# 3. Configuração do Admin de INSCRIÇÕES (UserEventos)
@admin.register(UserEventos)
class UserEventosAdmin(admin.ModelAdmin):
    list_display = ('user', 'evento', 'status', 'data_inscricao')
    list_filter = ('status', 'evento', 'data_inscricao')        # <--- ÓTIMO PARA VER PENDENTES
    search_fields = ('user__username', 'evento__nome')

# 4. Configuração do Admin de PERFIL (Opcional)
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo', 'celular')
    list_filter = ('tipo',)                                     # <--- FILTRA SE É PALESTRANTE/ALUNO
    search_fields = ('user__username', 'user__email')