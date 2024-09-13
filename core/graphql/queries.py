import graphene
from graphql import GraphQLError
from .types import ClienteType, ProjetoType, AtividadeType
from core.models import Cliente, Projeto, Atividade


class Query(graphene.ObjectType):
    """
    The Query object is responsible for the methods that
    will read data from the database.
    """

    # Cliente queries
    all_clientes = graphene.List(ClienteType)
    get_cliente = graphene.Field(ClienteType, id=graphene.Int(required=True))

    # Projeto queries
    all_projetos = graphene.List(ProjetoType)
    get_projeto = graphene.Field(ProjetoType, id=graphene.Int(required=True))
    get_projetos_by_cliente_id = graphene.List(
        ProjetoType, cliente_id=graphene.Int(required=True)
    )

    # Atividade queries
    all_atividades = graphene.List(AtividadeType)
    get_atividade = graphene.Field(AtividadeType, id=graphene.Int(required=True))
    get_atividades_by_projeto_id = graphene.List(
        AtividadeType, projeto_id=graphene.Int(required=True)
    )

    def resolve_all_clientes(self, info):
        """This method will return a list of clientes"""
        return Cliente.objects.all()

    def resolve_get_cliente(self, info, id):
        """This method will return a cliente from a cliente id"""
        try:
            return Cliente.objects.get(pk=id)
        except Cliente.DoesNotExist:
            raise GraphQLError("Cliente does not exist.")

    def resolve_all_projetos(self, info):
        """This method will return a list of projetos"""
        return Projeto.objects.all()

    def resolve_get_projeto(self, info, id):
        """This method will return a projeto from a projeto id"""
        try:
            return Projeto.objects.get(pk=id)
        except Projeto.DoesNotExist:
            raise GraphQLError("Projeto does not exist.")

    def resolve_get_projetos_by_cliente_id(self, info, cliente_id):
        """This method will return a list of projetos attached to a cliente"""
        try:
            return Projeto.objects.filter(cliente_id=cliente_id)
        except Projeto.DoesNotExist:
            return GraphQLError("No projetos found for this cliente.")
        except Exception as e:
            raise GraphQLError(f"Exception error: {str(e)}")

    def resolve_all_atividades(self, info):
        """This method will return a list of atividades"""
        return Atividade.objects.all()

    def resolve_get_atividade(self, info, id):
        """This method will return an atividade from an atividade id"""
        try:
            return Atividade.objects.get(pk=id)
        except Atividade.DoesNotExist:
            raise GraphQLError("Atividade does not exist.")

    def resolve_get_atividades_by_projeto_id(self, info, projeto_id):
        """This method will return a list of atividades attached to a projeto"""
        try:
            return Atividade.objects.filter(projeto_id=projeto_id)
        except Atividade.DoesNotExist:
            return GraphQLError("No atividades found for this projeto.")
        except Exception as e:
            raise GraphQLError(f"Exception error: {str(e)}")
