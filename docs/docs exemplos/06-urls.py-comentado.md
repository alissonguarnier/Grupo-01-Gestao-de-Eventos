# urls.py

## Arquivo comentado

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from core.views import UserViewSet, ProjetoViewSet, EquipeViewSet
```

- Importa os módulos necessários:
  - `admin` → painel administrativo padrão do Django.
  - `path`, `include` → funções para definir rotas (URLs).
  - `DefaultRouter` → cria automaticamente as rotas da API para os ViewSets.
  - `obtain_auth_token` → rota para autenticação via token (login na API).
  - `SpectacularAPIView`, `SpectacularSwaggerView`, `SpectacularRedocView` → rotas para gerar e exibir documentação da API (OpenAPI/Swagger/ReDoc).
- Importa os **ViewSets** que criamos (`UserViewSet`, `ProjetoViewSet`, `EquipeViewSet`).

### Registrando os ViewSets



```python
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'projetos', ProjetoViewSet)
router.register(r'equipes', EquipeViewSet)
```

- Cria um `DefaultRouter` que gera automaticamente as rotas CRUD para cada ViewSet.
- `router.register('users', UserViewSet)` → cria rotas como `/api/users/`.
- `router.register('projetos', ProjetoViewSet)` → cria rotas como `/api/projetos/`.
- `router.register('equipes', EquipeViewSet)` → cria rotas como `/api/equipes/`.

Isso evita escrever manualmente todas as rotas de CRUD.

### Definindo as rotas principais



```python
urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
```

- Rota para acessar o painel administrativo do Django (`/admin/`).



```python
    # API principal
    path('api/', include(router.urls)),
```

- Inclui todas as rotas geradas pelo `DefaultRouter` (users, projetos, equipes).
- Exemplo: `/api/users/`, `/api/projetos/`, `/api/equipes/`.



```python
    # Autenticação via token
    path('api/auth/token/', obtain_auth_token),
```

- Rota para autenticação via **token**.
- Usuário envia `username` e `password` → recebe um token para acessar a API.



```python
    # Schema OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
```

- Rota que gera o **schema OpenAPI** da API em formato JSON.
- Esse schema é usado pelas ferramentas de documentação.



```python
    # Documentação interativa
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),  # Swagger UI
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema')),  # Redoc
```

- `/api/docs/` → abre a documentação interativa com **Swagger UI** (permite testar endpoints direto no navegador).
- `/api/docs/redoc/` → abre a documentação alternativa com **ReDoc** (mais limpa e organizada para leitura).

## Resumindo para os alunos

- `/admin/` → painel administrativo do Django.
- `/api/` → rotas principais da API (users, projetos, equipes).
- `/api/auth/token/` → autenticação via token.
- `/api/schema/` → schema OpenAPI em JSON.
- `/api/docs/` → documentação interativa (Swagger).
- `/api/docs/redoc/` → documentação alternativa (ReDoc).