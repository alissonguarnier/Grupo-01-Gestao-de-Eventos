from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
'''
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from gestaoEventos.views import UserViewSet, ProjetoViewSet, EquipeViewSet
'''

'''
# Registrando os ViewSets diretamente aqui
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'projetos', ProjetoViewSet)
router.register(r'equipes', EquipeViewSet)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API principal
    path('api/', include(router.urls)),

    # Autenticação via token
    path('api/auth/token/', obtain_auth_token),

    # Schema OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Documentação interativa
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),  # Swagger UI
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema')),  # Redoc
]
'''