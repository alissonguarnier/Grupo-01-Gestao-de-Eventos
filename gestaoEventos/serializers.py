from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Perfil, Evento, Atividade, UserEventos

# ---------------------------------------------------------
# 1. Serializer de Inscrição (UserEventos)
# ---------------------------------------------------------

class UserEventosSerializer(serializers.ModelSerializer):
    user_nome = serializers.ReadOnlyField(source='user.username')
    evento_nome = serializers.ReadOnlyField(source='evento.nome')

    class Meta:
        model = UserEventos
        fields = ['id', 'user', 'user_nome', 'evento', 'evento_nome', 'data_inscricao', 'status']

# ---------------------------------------------------------
# 3. Serializer de Atividade
# ---------------------------------------------------------

class AtividadeSerializer(serializers.ModelSerializer):
    # Campos de leitura para mostrar nomes em vez de apenas IDs
    responsavel_nome = serializers.ReadOnlyField(source='responsavel.username')
    evento_titulo = serializers.ReadOnlyField(source='evento.nome')

    class Meta:
        model = Atividade
        fields = [
            'id', 'titulo', 'descricao', 'horario_inicio', 'horario_fim', 
            'tipo', 'evento', 'evento_titulo', 'responsavel', 'responsavel_nome'
        ]

# ---------------------------------------------------------
# 4. Serializer de Evento
# ---------------------------------------------------------

class EventoSerializer(serializers.ModelSerializer):
    # Mostra as atividades aninhadas dentro do evento (útil para detalhes)
    # read_only=True garante que não precisamos enviar atividades ao criar um evento
    atividades = AtividadeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Evento
        fields = [
            'id', 'nome', 'descricao', 'data_inicio', 'data_fim', 
            'local', 'atividades'
        ]

# ---------------------------------------------------------
# 2. Serializers de Usuário e Perfil (Participante)
# ---------------------------------------------------------

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ['celular', 'tipo']

class UserSerializer(serializers.ModelSerializer):
    # Aninhamos o perfil para que, ao chamar o User, venha os dados do Perfil junto
    perfil = PerfilSerializer()

    # Traz as inscrições (Eventos que ele participa)
    inscricoes = UserEventosSerializer(source='usereventos_set', many=True, read_only=True)
    
    # Traz as atividades que ele é responsável (Palestrante/Líder)
    atividades_lideradas = AtividadeSerializer(source='atividades_responsavel', many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'perfil', 'inscricoes', 'atividades_lideradas']
        # Adicionado 'inscricoes' e 'atividades_lideradas' na lista acima

    # Método create sobrescrito para salvar User e Perfil ao mesmo tempo
    def create(self, validated_data):
        perfil_data = validated_data.pop('perfil')
        # Cria o User padrão do Django
        user = User.objects.create(**validated_data)
        # Cria o Perfil linkado a esse User
        Perfil.objects.create(user=user, **perfil_data)
        return user

    # Método update para permitir atualizar dados de ambas as tabelas
    def update(self, instance, validated_data):
        perfil_data = validated_data.pop('perfil', None)
        
        # Atualiza campos do User
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        # Atualiza campos do Perfil se houver
        if perfil_data:
            perfil = instance.perfil
            perfil.celular = perfil_data.get('celular', perfil.celular)
            perfil.tipo = perfil_data.get('tipo', perfil.tipo)
            perfil.save()
            
        return instance

class EventoDashboardSerializer(serializers.ModelSerializer):
    """
    Serializer especial para a rota de Dashboard.
    Traz participantes e atividades tudo junto.
    """
    atividades = AtividadeSerializer(many=True, read_only=True)
    inscricoes = UserEventosSerializer(source='usereventos_set', many=True, read_only=True)
    
    class Meta:
        model = Evento
        fields = [
            'id', 'nome', 'data_inicio', 'local', 
            'atividades', 'inscricoes'
        ]