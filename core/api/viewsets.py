from rest_framework import viewsets
from core.models import Cliente, Projeto, Atividade
from .serializers import (
    ClienteModelSerializer,
    ProjetoModelSerializer,
    AtividadeModelSerializer,
)


class ClienteModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet for the Cliente model.
    Provides CRUD operations for Cliente using Django Rest Framework.
    """

    serializer_class = ClienteModelSerializer
    queryset = Cliente.objects.all()


class ProjetoModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet for the Projeto model.
    Provides CRUD operations for Cliente using Django Rest Framework.
    """

    serializer_class = ProjetoModelSerializer
    queryset = Projeto.objects.all()


class AtividadeModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet for the Atividade model.
    Provides CRUD operations for Cliente using Django Rest Framework.
    """

    serializer_class = AtividadeModelSerializer
    queryset = Atividade.objects.all()
