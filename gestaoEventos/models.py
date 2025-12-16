from django.db import models
from django.contrib.auth.models import User, Group # Supondo o uso do User padrão do Django


# 1. Tabela Users (Implícita ou Customizada)
# User padrão do Django, não precisa definir esta classe.

# 2. Tabela Perfil (Extensão do Users)
class Perfil(models.Model):
    tipos_usuario = [
        ('P', 'Participante'),
        ('C', 'Convidado'),
        ('O', 'Organizador'),
        ('X', 'Outros'),
    ]
    # ID_users (OneToOneField) – Relacionamento 1:1 com a Tabela Users [10]
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    tipo = models.CharField(max_length=1, choices=tipos_usuario, default='P')
    # O relacionamento com Eventos N:N não é colocado aqui, e sim na UserEventos.

    # ------ Grupo de acordo com o tipo ---------
    @property
    def is_grupo_participante(self):
        # Retorna True se for P, C ou X
        return self.tipo in ['P', 'C', 'X']

    @property
    def is_grupo_staff(self):
        # Retorna True se for O
        return self.tipo == 'O'
    
    # ---------------------------
    # Add automático nos grupos e cria o grupo se não tiver:
    # ---------------------------

    def save(self, *args, **kwargs):
        # 1. Salva os dados do Perfil primeiro
        super().save(*args, **kwargs)

        # 2. Define os nomes dos grupos (certificar que eles existem no Admin)
        grupo_participantes, _ = Group.objects.get_or_create(name='Participantes')
        grupo_staff, _ = Group.objects.get_or_create(name='Staff')

        # 3. Lógica para Adicionar/Remover baseada no tipo
        if self.is_grupo_participante:
            self.user.groups.add(grupo_participantes)
            self.user.groups.remove(grupo_staff) # Remove do outro para evitar conflito
            
        elif self.is_grupo_staff:
            self.user.groups.add(grupo_staff)
            self.user.groups.remove(grupo_participantes)
            
            # Opcional: Dar status de is_staff no User do Django se for Staff
            self.user.is_staff = True
            self.user.save()
        
        else:
            # Se não for nenhum (caso adicione outros tipos no futuro), limpa tudo
            self.user.groups.remove(grupo_participantes)
            self.user.groups.remove(grupo_staff)



# 3. Tabela Eventos
class Evento(models.Model):
    # Id (PK) é automático
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    local = models.CharField(max_length=255)
    
    # Relação N:N com User via UserEventos (through model)
    participantes = models.ManyToManyField(User, through='UserEventos', related_name='eventos_inscritos') 
    
    @property
    def carga_horaria_total(self):
        """
        Calcula a duração total somando (fim - inicio) de todas as atividades vinculadas.
        Retorna o valor em horas (arredondado).
        """
        total_segundos = 0
        
        # Pega todas as atividades desse evento
        for atividade in self.atividades.all():
            # Cria objetos dummy de data para poder subtrair os horários (que são TimeField)
            # Se seus campos forem DateTimeField, pode subtrair direto: atividade.horario_fim - atividade.horario_inicio
            
            # SUPONDO QUE SEJAM DateTimeField (o mais comum e recomendado):
            if atividade.horario_inicio and atividade.horario_fim:
                diff = atividade.horario_fim - atividade.horario_inicio
                total_segundos += diff.total_seconds()

        # Converte segundos para horas
        horas = total_segundos / 3600
        
        # Retorna inteiro (ex: 4) ou com 1 casa decimal (ex: 4.5) se preferir
        return round(horas)

    def __str__(self):
        return self.nome

# 4. Tabela Atividade
class Atividade(models.Model):
    # id (PK) é automático
    tipo_atividade = [
        ('W', 'Workshop'),
        ('P', 'Palestra'),
        ('O', 'Oficina'),
        ('X', 'Outros'),
    ]
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    horario_inicio = models.DateTimeField()
    horario_fim = models.DateTimeField()
    tipo = models.CharField(max_length=1, choices=tipo_atividade)
    
    # evento_fk (ForeignKey) – Relacionamento 1:N com Evento
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='atividades')
    
    # responsavel_id (ForeignKey) – Relacionamento 1:N com User (responsável pela atividade) 
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='atividades_responsavel') 
    
    def __str__(self):
        return f"{self.titulo} ({self.evento.nome})"

# 5. Tabela UserEventos (Tabela de Relacionamento N:N explícita)
class UserEventos(models.Model):
    status_inscrito = [
        ('C', 'Confirmado'),
        ('P', 'Pendente'),
        ('X', 'Outros'),
    ]
    # ID (PK) é automático
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Id_users 
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE) # id_eventos 
    data_inscricao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=status_inscrito, default='C')
    
    class Meta:
        # Garante que um usuário só pode se inscrever uma vez em um evento específico
        unique_together = ('user', 'evento')

        # Adiciona os nomes bonitos para o Admin
        verbose_name = "Inscrição"
        verbose_name_plural = "Inscrições"