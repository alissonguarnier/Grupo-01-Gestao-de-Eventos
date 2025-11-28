'''from django.db import models
from django.contrib.auth.models import User


class Projeto(models.Model):
    STATUS_CHOICES = [
        ('planejado', 'Planejado'),
        ('andamento', 'Em andamento'),
        ('concluido', 'Concluído'),
    ]
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    cliente = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planejado')
    data_inicio = models.DateField()
    data_fim_prevista = models.DateField()

    def __str__(self):
        return self.titulo

    @property
    def participantes(self):
        """Retorna todos os usuários que participam das equipes do projeto."""
        return User.objects.filter(equipes__projeto=self).distinct()


class Equipe(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name="equipes")
    lider = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="lidera_equipe")
    membros = models.ManyToManyField(User, related_name="equipes")

    def __str__(self):
        return f"{self.nome} ({self.projeto.titulo})"

        ### CÓDIGO ANTIGO DE EXEMPLO COMENTADO PARA REFERÊNCIA ###
'''

from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    TIPO_CHOICES = [
        ('PARTICIPANTE', 'Participante'),
        ('CONVIDADO', 'Convidado'),
        ('ORGANIZADOR', 'Organizador'),
    ]
    
    # Relacionamento 1 para 1 com o Usuário padrão do Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    celular = models.CharField(max_length=20, blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='PARTICIPANTE')

    def __str__(self):
        return f"{self.user.username} - {self.tipo}"

class Evento(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()  
    data_inicio = models.DateField() # Python usa snake_case (com underline)
    data_fim = models.DateField()
    local = models.CharField(max_length=200)
    
    # A classe "UsersEventos" do diagrama vira este campo ManyToMany
    participantes = models.ManyToManyField(User, related_name='eventos_participados', blank=True)

    def __str__(self):
        return self.nome

class Atividade(models.Model):
    TIPO_ATIVIDADE_CHOICES = [
        ('WORKSHOP', 'Workshop'),
        ('PALESTRA', 'Palestra'),
        ('OFICINA', 'Oficina'),
        ('OUTROS', 'Outros'),
    ]
    
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    tipo = models.CharField(max_length=20, choices=TIPO_ATIVIDADE_CHOICES)
    
    # Relacionamentos (Foreign Keys)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='atividades')
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='atividades_responsaveis')

    def __str__(self):
        return self.titulo
