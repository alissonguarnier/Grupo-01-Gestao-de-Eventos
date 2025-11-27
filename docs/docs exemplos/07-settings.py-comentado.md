# settings.py

## Arquivo parcial comentado



```python
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
```

- **INSTALLED_APPS** → lista de aplicativos que o Django vai carregar.
- Os primeiros são **apps padrão do Django**:
  - `admin` → painel administrativo.
  - `auth` → sistema de autenticação (usuários, login, senha).
  - `contenttypes` → suporte para tipos de conteúdo genéricos.
  - `sessions` → controle de sessões (login persistente).
  - `messages` → sistema de mensagens temporárias.
  - `staticfiles` → gerenciamento de arquivos estáticos (CSS, JS, imagens).



```python
    # DRF
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular_sidecar',
    'drf_spectacular',
```

- **Apps do Django REST Framework (DRF)**:
  - `rest_framework` → núcleo do DRF, permite criar APIs.
  - `rest_framework.authtoken` → adiciona suporte a autenticação via **token**.
  - `drf_spectacular_sidecar` → fornece arquivos estáticos para documentação (Swagger/ReDoc).
  - `drf_spectacular` → gera automaticamente o **schema OpenAPI** da API.



```python
    # Nosso app
    'core',
]
```

- `core` → nosso aplicativo principal, onde estão os modelos, views, serializers etc. 👉 É aqui que construímos o sistema de projetos, equipes e usuários.

### Configuração do DRF



```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```

- `DEFAULT_AUTHENTICATION_CLASSES` → define como os usuários vão se autenticar na API.
  - Aqui usamos **TokenAuthentication** → cada usuário recebe um token para acessar a API.
- `DEFAULT_SCHEMA_CLASS` → define como o DRF gera o **schema da API**.
  - Usamos `drf_spectacular.openapi.AutoSchema` → gera automaticamente a documentação OpenAPI.

### Configuração do drf-spectacular



```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'DevLab Project API',
    'DESCRIPTION': 'Sistema de Gestão de Projetos Colaborativos para coordenadores, professores e estudantes.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
```

- `TITLE` → título da documentação da API.
- `DESCRIPTION` → descrição que aparece na documentação (explica o sistema)(aceita markdown, é possível montar uma string maior em markdown).
- `VERSION` → versão da API.
- `SERVE_INCLUDE_SCHEMA` → se `False`, o schema não aparece embutido na documentação (apenas endpoints).

## Resumindo para os alunos

- **INSTALLED_APPS** → lista de apps carregados pelo Django (padrão, DRF e nosso `core`).
- **REST_FRAMEWORK** → configura autenticação e geração de schema da API.
- **SPECTACULAR_SETTINGS** → personaliza a documentação da API (Swagger/ReDoc).