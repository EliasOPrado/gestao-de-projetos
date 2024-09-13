from graphene_django import DjangoObjectType
from core.models import Cliente, Projeto, Atividade


class ClienteType(DjangoObjectType):
    """
    GraphQL type for the Cliente model.

    This class maps the User Django model to a GraphQL type, making it accessible
    in GraphQL queries and mutations.
    """

    class Meta:
        model = Cliente
        field = "__all__"


class ProjetoType(DjangoObjectType):
    """
    GraphQL type for the Projeto model.

    This class maps the User Django model to a GraphQL type, making it accessible
    in GraphQL queries and mutations.
    """

    class Meta:
        model = Projeto
        field = "__all__"


class AtividadeType(DjangoObjectType):
    """
    GraphQL type for the Atividade model.

    This class maps the User Django model to a GraphQL type, making it accessible
    in GraphQL queries and mutations.
    """

    class Meta:
        model = Atividade
        field = "__all__"
