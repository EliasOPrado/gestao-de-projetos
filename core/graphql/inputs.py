import graphene


class ClienteInput(graphene.InputObjectType):
    """Input object type for cliente-related mutations in the GraphQL API."""

    nome = graphene.String(required=True)
    email = graphene.String(required=True)
    telefone = graphene.String()


class ProjetoInput(graphene.InputObjectType):
    """Input object type for projeto-related mutations in the GraphQL API."""

    nome = graphene.String(required=True)
    descricao = graphene.String()
    cliente_id = graphene.ID(required=True)
    status = graphene.String()


class AtividadeInput(graphene.InputObjectType):
    """Input object type for atividade-related mutations in the GraphQL API."""

    projeto_id = graphene.ID(required=True)
    descricao = graphene.String(required=True)
    prazo = graphene.Date(required=True)
