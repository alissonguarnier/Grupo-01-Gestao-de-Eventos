from django.db import models
from django.contrib.auth.models import User

'''
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
