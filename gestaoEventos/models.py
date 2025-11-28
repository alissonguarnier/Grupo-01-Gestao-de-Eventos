'''
from django.db import models
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
'''

# ---------------------------- Código a partir daqui -----------------------------


from django.db import models
from django.contrib.auth.models import User # Supondo o uso do User padrão do Django

# 1. Tabela Users (Implícita ou Customizada)
# User padrão do Django, não precisa definir esta classe.

# 2. Tabela Perfil (Extensão do Users)
class Perfil(models.Model):
    TIPOS_USUARIO = [
        ('P', 'Participante'),
        ('C', 'Convidado'),
        ('O', 'Organizador'),
        ('X', 'Outros'),
    ]
    # ID_users (OneToOneField) – Relacionamento 1:1 com a Tabela Users [10]
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    tipo = models.CharField(max_length=1, choices=TIPOS_USUARIO, default='P')
    # O relacionamento com Eventos N:N não é colocado aqui, e sim na UserEventos.

# 3. Tabela Eventos
class Evento(models.Model):
    # Id (PK) é automático
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    data_inicio = models.DateField() # Ou usar DateTimeField?
    data_fim = models.DateField()
    local = models.CharField(max_length=255)
    
    # Relação N:N com User via UserEventos (through model)
    participantes = models.ManyToManyField(User, through='UserEventos', related_name='eventos_inscritos') 
    
    def __str__(self):
        return self.nome

# 4. Tabela Atividade
class Atividade(models.Model):
    # id (PK) é automático
    TIPO_ATIVIDADE = [
        ('W', 'Workshop'),
        ('P', 'Palestra'),
        ('O', 'Oficina'),
        ('X', 'Outros'),
    ]
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    tipo = models.CharField(max_length=1, choices=TIPO_ATIVIDADE)
    
    # evento_fk (ForeignKey) – Relacionamento 1:N com Evento
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='atividades')
    
    # responsavel_id (ForeignKey) – Relacionamento 1:N com User (responsável pela atividade) 
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='atividades_responsavel') 
    
    def __str__(self):
        return f"{self.titulo} ({self.evento.nome})"

# 5. Tabela UserEventos (Tabela de Relacionamento N:N explícita)
class UserEventos(models.Model):
    # ID (PK) é automático
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Id_users [10]
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE) # id_eventos [10]
    data_inscricao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Confirmado')
    
    class Meta:
        # Garante que um usuário só pode se inscrever uma vez em um evento específico
        unique_together = ('user', 'evento')