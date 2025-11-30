from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic import RedirectView

# Importações do Spectacular
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# Importações das suas Views (Use os nomes do seu projeto)
from gestaoEventos.views import EventoViewSet, AtividadeViewSet, UserViewSet

# Configuração do Router
router = DefaultRouter()
router.register(r'eventos', EventoViewSet, basename='evento')
router.register(r'atividades', AtividadeViewSet, basename='atividade')
router.register(r'participantes', UserViewSet, basename='participante')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)), # Suas rotas funcionais

    # Redireciona a raiz (/) para a documentação (/api/docs/)
    path('', RedirectView.as_view(url='/api/docs/', permanent=False)),

    # --- ROTAS DE DOCUMENTAÇÃO (SPECTACULAR) ---
    
    # 1. Rota que gera o arquivo YAML/JSON (o "coração" da doc)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # 2. Rota visual SWAGGER (A interface bonita azul/verde)
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # 3. Rota visual REDOC (Uma interface alternativa mais limpa)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]