from rest_framework import viewsets
from core.models import Cliente, Projeto, Atividade
from .serializers import (
    ClienteModelSerializer,
    ProjetoModelSerializer,
    AtividadeModelSerializer,
)


class ClienteModelViewSet(viewsets.ModelViewSet):
    serializer_class = ClienteModelSerializer
    queryset = Cliente.objects.all()


class ProjetoModelViewSet(viewsets.ModelViewSet):
    serializer_class = ProjetoModelSerializer
    queryset = Projeto.objects.all()


class AtividadeModelViewSet(viewsets.ModelViewSet):
    serializer_class = AtividadeModelSerializer
    queryset = Atividade.objects.all()
