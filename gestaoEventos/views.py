from rest_framework import viewsets, permissions
'from rest_framework.decorators import action'
'from rest_framework.response import Response'
'from django.contrib.auth.models import User'
'from .models import Projeto, Equipe'
'from .serializers import UserSerializer, ProjetoSerializer, EquipeSerializer'

'''
# -------------------------------
# USERS
# -------------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def projetos(self, request, pk=None):
        user = self.get_object()
        projetos = Projeto.objects.filter(equipes__membros=user).distinct()
        serializer = ProjetoSerializer(projetos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def equipes(self, request, pk=None):
        user = self.get_object()
        equipes = user.equipes.all()
        serializer = EquipeSerializer(equipes, many=True)
        return Response(serializer.data)

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


# -------------------------------
# PROJETOS
# -------------------------------
class ProjetoViewSet(viewsets.ModelViewSet):
    queryset = Projeto.objects.all()
    serializer_class = ProjetoSerializer

    def get_permissions(self):
        # Apenas staff pode criar, editar ou excluir
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        # Usuário comum só pode listar/consultar
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Projeto.objects.all()
        # Projetos em que o usuário participa via equipes
        return Projeto.objects.filter(equipes__membros=user).distinct()

    @action(detail=True, methods=['get'])
    def equipes(self, request, pk=None):
        projeto = self.get_object()
        serializer = EquipeSerializer(projeto.equipes.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def participantes(self, request, pk=None):
        projeto = self.get_object()
        users = User.objects.filter(equipes__projeto=projeto).distinct()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

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


# -------------------------------
# EQUIPES
# -------------------------------
class EquipeViewSet(viewsets.ModelViewSet):
    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer

    def get_permissions(self):
        # Apenas staff pode criar, editar ou excluir
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'definir_lider']:
            return [permissions.IsAdminUser()]
        # Usuário comum só pode listar/consultar
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Equipe.objects.all()
        # Usuário comum só vê as equipes em que participa
        return Equipe.objects.filter(membros=user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def definir_lider(self, request, pk=None):
        equipe = self.get_object()
        user_id = request.data.get("user_id")
        try:
            user = User.objects.get(id=user_id)
            # regra: líder também deve ser membro
            if user not in equipe.membros.all():
                return Response({"error": "O líder deve estar cadastrado como membro da equipe."}, status=400)
            equipe.lider = user
            equipe.save()
            return Response({"status": f"{user.username} agora é líder da equipe {equipe.nome}"})
        except User.DoesNotExist:
            return Response({"error": "Usuário não encontrado"}, status=400)
'''