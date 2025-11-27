# views.py

## Arquivo comentado

```python
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Projeto, Equipe
from .serializers import UserSerializer, ProjetoSerializer, EquipeSerializer
```

- Importa as ferramentas do **Django REST Framework**:
  - `viewsets` → cria conjuntos de views (CRUD completo).
  - `permissions` → controla quem pode acessar cada rota.
  - `action` → cria rotas personalizadas além do CRUD padrão.
  - `Response` → retorna respostas em formato JSON.
- Importa os modelos/tabelas  (`Projeto`, `Equipe`) e os serializers correspondentes.
- Importa o modelo/tabela `User` do Django.

## UserViewSet



```python
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
```

- `ModelViewSet` → cria automaticamente rotas CRUD para usuários.
- `queryset` → todos os usuários.
- `serializer_class` → usa `UserSerializer` para transformar em JSON.
- `permission_classes` → só **admin/staff** pode acessar o CRUD de usuários.

### Rotas personalizadas de User



```python
    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def projetos(self, request, pk=None):
        user = self.get_object()
        projetos = Projeto.objects.filter(equipes__membros=user).distinct()
        serializer = ProjetoSerializer(projetos, many=True)
        return Response(serializer.data)
```

- Rota: `GET /api/users/{id}/projetos/`
- Mostra todos os projetos em que o usuário participa (via equipes).
- `distinct()` → evita duplicados.



```python
    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def equipes(self, request, pk=None):
        user = self.get_object()
        equipes = user.equipes.all()
        serializer = EquipeSerializer(equipes, many=True)
        return Response(serializer.data)
```

- Rota: `GET /api/users/{id}/equipes/`
- Mostra todas as equipes em que o usuário está.



```python
    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def visao_geral(self, request, pk=None):
        user = self.get_object()
        projetos = Projeto.objects.filter(equipes__membros=user).distinct()
        equipes = user.equipes.all()
        data = {
            "usuario": UserSerializer(user).data,
            "projetos": ProjetoSerializer(projetos, many=True).data,
            "equipes": EquipeSerializer(equipes, many=True).data,
        }
        return Response(data)
```

- Rota: `GET /api/users/{id}/visao_geral/`
- Retorna um resumo completo: dados do usuário, projetos e equipes.

## ProjetoViewSet



```python
class ProjetoViewSet(viewsets.ModelViewSet):
    queryset = Projeto.objects.all()
    serializer_class = ProjetoSerializer
```

- CRUD de projetos.
- Usa `ProjetoSerializer`.

### Permissões



```python
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
```

- Apenas **admin/staff** pode criar, editar ou excluir projetos.
- Usuário comum só pode listar e consultar.

### Queryset filtrado



```python
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Projeto.objects.all()
        return Projeto.objects.filter(equipes__membros=user).distinct()
```

- Admin vê todos os projetos.
- Usuário comum vê apenas os projetos em que participa (via equipes).

### Rotas personalizadas de Projeto



```python
    @action(detail=True, methods=['get'])
    def equipes(self, request, pk=None):
        projeto = self.get_object()
        serializer = EquipeSerializer(projeto.equipes.all(), many=True)
        return Response(serializer.data)
```

- Rota: `GET /api/projetos/{id}/equipes/`
- Lista todas as equipes do projeto.



```python
    @action(detail=True, methods=['get'])
    def participantes(self, request, pk=None):
        projeto = self.get_object()
        users = User.objects.filter(equipes__projeto=projeto).distinct()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
```

- Rota: `GET /api/projetos/{id}/participantes/`
- Lista todos os usuários que participam do projeto (via equipes).



```python
    @action(detail=True, methods=['get'])
    def dashboard(self, request, pk=None):
        projeto = self.get_object()
        data = {
            "projeto": ProjetoSerializer(projeto).data,
            "equipes": EquipeSerializer(projeto.equipes.all(), many=True).data,
            "participantes": UserSerializer(
                User.objects.filter(equipes__projeto=projeto).distinct(),
                many=True
            ).data,
        }
        return Response(data)
```

- Rota: `GET /api/projetos/{id}/dashboard/`
- Retorna um resumo completo: dados do projeto, equipes e participantes.

## EquipeViewSet



```python
class EquipeViewSet(viewsets.ModelViewSet):
    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer
```

- CRUD de equipes.
- Usa `EquipeSerializer`.

### Permissões



```python
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'definir_lider']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
```

- Apenas **admin/staff** pode criar, editar, excluir ou definir líder.
- Usuário comum só pode listar/consultar.

### Queryset filtrado



```python
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Equipe.objects.all()
        return Equipe.objects.filter(membros=user)
```

- Admin vê todas as equipes.
- Usuário comum vê apenas as equipes em que participa.

### Rota personalizada de Equipe



```python
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def definir_lider(self, request, pk=None):
        equipe = self.get_object()
        user_id = request.data.get("user_id")
        try:
            user = User.objects.get(id=user_id)
            if user not in equipe.membros.all():
                return Response({"error": "O líder deve estar cadastrado como membro da equipe."}, status=400)
            equipe.lider = user
            equipe.save()
            return Response({"status": f"{user.username} agora é líder da equipe {equipe.nome}"})
        except User.DoesNotExist:
            return Response({"error": "Usuário não encontrado"}, status=400)
```

- Rota: `POST /api/equipes/{id}/definir_lider/`
- Define o líder da equipe.
- Regra: o líder deve estar cadastrado como membro.
- Apenas **admin/staff** pode executar.

## Resumindo 

- **UserViewSet** → rotas para ver projetos, equipes e visão geral de um usuário.
- **ProjetoViewSet** → rotas para listar projetos, equipes, participantes e dashboard.
- **EquipeViewSet** → rotas para listar equipes e definir líder.
- **Permissões** → garantem que só admin pode criar/editar/excluir, enquanto usuários comuns só consultam.