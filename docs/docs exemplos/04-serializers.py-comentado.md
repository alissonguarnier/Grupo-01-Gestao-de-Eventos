#  **serializers.py**

## **Arquivo comentado**

```python
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Projeto, Equipe
```

- `rest_framework import serializers` → importa as classes do Django REST Framework para transformar modelos em JSON (serialização) e vice-versa (desserialização).
- `User` → modelo/tabela de usuário padrão do Django.
- `Projeto` e `Equipe` → nossos modelos/tabelas criados anteriormente.
- 

## USER SERIALIZER

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
```

- `ModelSerializer` → cria automaticamente um serializer baseado no modelo.

- Aqui escolhemos apenas os campos `id`, `username` e `email` para expor na API.  Isso evita mostrar dados sensíveis como senha que também existem neta tabela.

  

## PROJETO SERIALIZER

```python
class ProjetoSerializer(serializers.ModelSerializer):
    # participantes calculados a partir das equipes
    participantes = serializers.SerializerMethodField()
```

- `SerializerMethodField` → cria um campo calculado, que não existe diretamente no modelo.
- Aqui usamos para listar os **participantes do projeto** (derivados das equipes).



```python
    class Meta:
        model = Projeto
        fields = [
            'id',
            'titulo',
            'descricao',
            'cliente',
            'status',
            'data_inicio',
            'data_fim_prevista',
            'participantes', # nao existe na tabela por isso precisa ser expecificado aqui
        ]
```

- Define quais campos do modelo `Projeto` serão expostos na API.
- Incluímos o campo calculado `participantes`.



```python
    def get_participantes(self, obj):
        # pega todos os membros das equipes do projeto
        users = User.objects.filter(equipes__projeto=obj).distinct()
        return UserSerializer(users, many=True).data
```

- Método que alimenta o campo `participantes`.
- Busca todos os usuários que estão em equipes ligadas ao projeto (`equipes__projeto=obj`).
- `distinct()` → evita duplicados.
- Serializa os usuários com `UserSerializer`.  Assim, cada projeto retorna automaticamente seus participantes.



## EQUIPE SERIALIZER



```python
class EquipeSerializer(serializers.ModelSerializer):
    membros = UserSerializer(many=True, read_only=True)
```

- `membros` → lista de usuários da equipe.
- `read_only=True` → só leitura, não pode ser alterado diretamente via API.
- Usa `UserSerializer` para mostrar os dados básicos de cada membro.



```python
    membros_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        source='membros'
    )
```

- Campo auxiliar para **inserir membros** na equipe via IDs.
- `write_only=True` → usado apenas na escrita (não aparece na resposta da API).
- `source='membros'` → conecta esse campo ao relacionamento `membros` do modelo.  Permite enviar algo como `"membros_ids": [2, 3]` para adicionar usuários.



```python
    lider = UserSerializer(read_only=True)
```

- Mostra os dados do líder da equipe.
- `read_only=True` → não pode ser alterado diretamente.



```python
    lider_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='lider',
        required=False
    )
```

- Campo auxiliar para **definir o líder** via ID.
- `write_only=True` → usado apenas na escrita.
- `source='lider'` → conecta ao campo `lider` do modelo.
- `required=False` → não é obrigatório (a equipe pode ser criada sem líder inicialmente).



```python
    class Meta:
        model = Equipe
        fields = [
            'id',
            'nome',
            'descricao',
            'projeto',
            'lider',
            'lider_id',
            'membros',
            'membros_ids',
        ]
```

- Define os campos expostos na API para `Equipe`.
- Inclui tanto os campos de leitura (`lider`, `membros`) quanto os auxiliares de escrita (`lider_id`, `membros_ids`).  Isso dá flexibilidade: a API mostra os dados completos, mas aceita apenas IDs para criar/editar.

## Resumindo

- **UserSerializer** → mostra dados básicos do usuário.
- **ProjetoSerializer** → mostra dados do projeto + participantes calculados automaticamente.
- **EquipeSerializer** → mostra dados da equipe, líder e membros.
  - Para **criar/editar**, usamos `lider_id` e `membros_ids`.
  - Para **consultar**, vemos `lider` e `membros` já detalhados.