from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic import RedirectView
from rest_framework.authtoken.views import obtain_auth_token

# Importações do Spectacular
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# Importações das suas Views (Use os nomes do seu projeto)
from gestaoEventos.views import EventoViewSet, AtividadeViewSet, UserViewSet

# --- FORÇAR O LOGIN ---
from django.contrib.auth import logout
from django.shortcuts import redirect
# -------------------------

# --- FUNÇÃO PARA FORÇAR LOGIN ---
def admin_logout_login(request):
    """
    1. Remove a sessão atual (desloga o admin).
    2. Redireciona para a tela de login limpa.
    """
    logout(request) 
    return redirect('/admin/login/')
# ---------------------

# Configuração do Router
router = DefaultRouter()
router.register(r'eventos', EventoViewSet, basename='evento')
router.register(r'atividades', AtividadeViewSet, basename='atividade')
router.register(r'participantes', UserViewSet, basename='participante')

# --- PERSONALIZAÇÃO DO ADMIN ---
admin.site.site_header = "Administração EventLab"  # Texto no topo do Login e da Dashboard
admin.site.site_title = "EventLab Admin"           # Texto na aba do navegador
admin.site.index_title = "Gestão de Eventos - Projeto Integrador"       # Texto na lista de apps (Home do Admin)

# -------------------------------

urlpatterns = [
    path('admin/entrar/', admin_logout_login, name='admin_force_login'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)), # Suas rotas funcionais

    # Redireciona a raiz (/) para a documentação (/api/docs/)
    path('', RedirectView.as_view(url='/api/docs/', permanent=False)),

    # --- ROTA PARA PEGAR O TOKEN (LOGIN) ---
    path('api/auth/token/', obtain_auth_token, name='api_token_auth'),
    # ---------------------------------------

    # --- ROTAS DE DOCUMENTAÇÃO (SPECTACULAR) ---
    
    # 1. Rota que gera o arquivo YAML/JSON (o "coração" da doc)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # 2. Rota visual SWAGGER (A interface bonita azul/verde)
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # 3. Rota visual REDOC (Uma interface alternativa mais limpa)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]