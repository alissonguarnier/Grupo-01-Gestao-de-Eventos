# models.py

## Arquivo comentado



```python
from django.db import models
from django.contrib.auth.models import User
```

- `django.db import models` → importa as classes base para criar modelos no Django (como `CharField`, `TextField`, `ForeignKey` etc.).
- `django.contrib.auth.models import User` → importa o modelo de usuário padrão do Django, que já vem pronto com login, senha, email, etc. Assim não precisamos criar uma tabela de usuários do zero.

### Modelo/Tabela **Projeto**



```python
class Projeto(models.Model):
```

- Define uma classe chamada `Projeto`, que herda de `models.Model`.
- Isso significa que o Django vai criar uma tabela chamada `projeto` no banco de dados.



```python
    STATUS_CHOICES = [
        ('planejado', 'Planejado'),
        ('andamento', 'Em andamento'),
        ('concluido', 'Concluído'),
    ]
```

- Lista de opções para o campo `status`.
- O primeiro valor é o que será salvo no banco (`planejado`, `andamento`, `concluido`).
- O segundo valor é o texto amigável que aparece no admin do Django (uma lista para escolha).



```python
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    cliente = models.CharField(max_length=100)
```

- `titulo` → texto curto (até 100 caracteres).
- `descricao` → texto longo, sem limite definido.
- `cliente` → nome do cliente do projeto.



```python
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planejado')
```

- Campo de texto com **escolhas limitadas** (`choices`).
- Valor padrão é `'planejado'`.



```python
    data_inicio = models.DateField()
    data_fim_prevista = models.DateField()
```

- Datas de início e fim previstas do projeto.
- `DateField` armazena apenas a data (sem hora).



```python
    def __str__(self):
        return self.titulo
```

- Método especial que define como o objeto aparece no admin ou no shell.
- Exemplo: em vez de mostrar `Projeto object (1)`, vai mostrar o título do projeto.



```python
    @property
    def participantes(self):
        """Retorna todos os usuários que participam das equipes do projeto."""
        return User.objects.filter(equipes__projeto=self).distinct()
```

- `@property` → transforma o método em um **atributo calculado**.

- Busca todos os usuários que estão em equipes ligadas a este projeto.

- `distinct()` → evita duplicados (se o mesmo usuário estiver em mais de uma equipe do projeto).  Isso significa que os **participantes do projeto não são salvos diretamente**, mas derivados das equipes.

  

### Modelo/Tabela **Equipe**



```python
class Equipe(models.Model):
```

- Define a tabela de equipes.
- Cada equipe pertence a um projeto e tem membros.



```python
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
```

- Nome e descrição da equipe.



```python
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name="equipes")
```

- `ForeignKey` → cria uma relação **1:N** (um projeto pode ter várias equipes).
- `on_delete=models.CASCADE` → se o projeto for apagado, todas as equipes ligadas a ele também serão apagadas.
- `related_name="equipes"` → permite acessar as equipes de um projeto com `projeto.equipes.all()`.



```python
    lider = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="lidera_equipe")
```

- `OneToOneField` → relação **1:1** (uma equipe tem um líder único, e um usuário só pode liderar uma equipe).
- `on_delete=models.SET_NULL` → se o líder for apagado, o campo fica `NULL` em vez de apagar a equipe.
- `null=True, blank=True` → o campo pode ficar vazio.
- `related_name="lidera_equipe"` → permite acessar a equipe que o usuário lidera com `user.lidera_equipe`.



```python
    membros = models.ManyToManyField(User, related_name="equipes")
```

- `ManyToManyField` → relação **N:N** (uma equipe pode ter vários membros, e um usuário pode estar em várias equipes).
- `related_name="equipes"` → permite acessar todas as equipes de um usuário com `user.equipes.all()`.



```python
    def __str__(self):
        return f"{self.nome} ({self.projeto.titulo})"
```

- Mostra o nome da equipe junto com o título do projeto.

  

## Resumindo 

- **Projeto** → agrupa várias equipes.
- **Equipe** → pertence a um projeto, tem vários membros e um líder.
- **User** → pode estar em várias equipes e pode liderar uma delas.
- **Participantes do projeto** → são calculados automaticamente a partir dos membros das equipes.
