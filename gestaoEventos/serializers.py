'''
#core/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
'from .models import Projeto, Equipe'


# -------------------------------
# USER
# -------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# -------------------------------
# PROJETO
# -------------------------------
class ProjetoSerializer(serializers.ModelSerializer):
    # participantes calculados a partir das equipes
    participantes = serializers.SerializerMethodField()

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
            'participantes',
        ]

    def get_participantes(self, obj):
        # pega todos os membros das equipes do projeto
        users = User.objects.filter(equipes__projeto=obj).distinct()
        return UserSerializer(users, many=True).data


# -------------------------------
# EQUIPE
# -------------------------------
class EquipeSerializer(serializers.ModelSerializer):
    membros = UserSerializer(many=True, read_only=True)
    membros_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        source='membros'
    )
    lider = UserSerializer(read_only=True)
    lider_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='lider',
        required=False
    )

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
        ### CÓDIGO ANTIGO DE EXEMPLO COMENTADO PARA REFERÊNCIA ###
'''
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Perfil, Evento, Atividade

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class PerfilSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Perfil
        fields = '__all__'

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'

class AtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atividade
        fields = '__all__'