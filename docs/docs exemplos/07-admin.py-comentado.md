# admin.py

## Arquivo comentado



```python
from django.contrib import admin
from .models import Projeto, Equipe
from rest_framework.authtoken.models import Token
```

- `django.contrib import admin` → importa o sistema de administração do Django.
- `.models import Projeto, Equipe` → importa os modelos que criamos para poder registrá-los no admin.
- `rest_framework.authtoken.models import Token` → importa o modelo de **Token de autenticação** do Django REST Framework.  Esse modelo guarda os tokens de login dos usuários quando usamos autenticação via token.



```python
admin.site.register(Projeto)
admin.site.register(Equipe)
admin.site.register(Token)
```

- `admin.site.register(...)` → registra o modelo no painel administrativo do Django.
- Isso significa que os administradores poderão **visualizar, criar, editar e excluir** registros desses modelos diretamente pelo `/admin/`.
- Registramos:
  - **Projeto** → para gerenciar os projetos.
  - **Equipe** → para gerenciar as equipes vinculadas aos projetos.
  - **Token** → para visualizar e administrar os tokens de autenticação dos usuários.

## Resumindo para os alunos

- O arquivo `admin.py` serve para **registrar os modelos no painel administrativo** do Django.
- Assim, o professor ou administrador pode gerenciar **Projetos**, **Equipes** e **Tokens de autenticação** sem precisar usar a API diretamente.
- É uma forma prática de administrar os dados pelo navegador, usando a interface padrão do Django.