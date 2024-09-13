import graphene
from .types import ClienteType, ProjetoType, AtividadeType
from .inputs import ClienteInput, ProjetoInput, AtividadeInput
from core.models import Cliente, Projeto, Atividade


class CreateClienteMutation(graphene.Mutation):
    """
    Mutation for creating a new Cliente using the GraphQL API.
    """

    class Arguments:
        input = ClienteInput(required=True)

    cliente = graphene.Field(ClienteType)

    def mutate(self, info, input):
        cliente = Cliente.objects.create(**input)
        return CreateClienteMutation(cliente=cliente)


class UpdateClienteMutation(graphene.Mutation):
    """
    Mutation for updating an existing Clinete using the GraphQL API.
    """

    class Arguments:
        id = graphene.ID(required=True)
        input = ClienteInput(required=True)

    cliente = graphene.Field(ClienteType)

    def mutate(self, info, id, input):
        cliente = Cliente.objects.get(pk=id)
        for attr, value in input.items():
            setattr(cliente, attr, value)
        cliente.save()
        return UpdateClienteMutation(cliente=cliente)


class DeleteClienteMutation(graphene.Mutation):
    """
    Mutation for deleting an existing Clinete using the GraphQL API.
    """

    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            cliente = Cliente.objects.get(pk=id)
            cliente.delete()
            return DeleteClienteMutation(success=True)
        except Cliente.DoesNotExist:
            return DeleteClienteMutation(success=False)


class CreateProjetoMutation(graphene.Mutation):
    """
    Mutation for creating a Projeto using the GraphQL API.
    """

    class Arguments:
        input = ProjetoInput(required=True)

    projeto = graphene.Field(ProjetoType)

    def mutate(self, info, input):
        cliente = Cliente.objects.get(pk=input.pop("cliente_id"))
        projeto = Projeto.objects.create(cliente=cliente, **input)
        return CreateProjetoMutation(projeto=projeto)


class UpdateProjetoMutation(graphene.Mutation):
    """
    Mutation for updating an existing Projeto using the GraphQL API.
    """

    class Arguments:
        id = graphene.ID(required=True)
        input = ProjetoInput(required=True)

    projeto = graphene.Field(ProjetoType)

    def mutate(self, info, id, input):
        projeto = Projeto.objects.get(pk=id)
        for attr, value in input.items():
            setattr(projeto, attr, value)
        projeto.save()
        return UpdateProjetoMutation(projeto=projeto)


class DeleteProjetoMutation(graphene.Mutation):
    """
    Mutation for deleting an existing Projeto using the GraphQL API.
    """

    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            projeto = Projeto.objects.get(pk=id)
            projeto.delete()
            return DeleteProjetoMutation(success=True)
        except Projeto.DoesNotExist:
            return DeleteProjetoMutation(success=False)


class CreateAtividade(graphene.Mutation):
    """
    Mutation for creating an Atividade using the GraphQL API.
    """

    class Arguments:
        input = AtividadeInput(required=True)

    atividade = graphene.Field(AtividadeType)

    def mutate(self, info, input):
        projeto = Projeto.objects.get(pk=input.pop("projeto_id"))
        atividade = Atividade.objects.create(projeto=projeto, **input)
        return CreateAtividade(atividade=atividade)


class UpdateAtividadeMutation(graphene.Mutation):
    """
    Mutation for updating an Atividade using the GraphQL API.
    """

    class Arguments:
        id = graphene.ID(required=True)
        input = AtividadeInput(required=True)

    atividade = graphene.Field(AtividadeType)

    def mutate(self, info, id, input):
        atividade = Atividade.objects.get(pk=id)
        for attr, value in input.items():
            setattr(atividade, attr, value)
        atividade.save()
        return UpdateAtividadeMutation(atividade=atividade)


class DeleteAtividadeMutation(graphene.Mutation):
    """
    Mutation for deleting an Atividade using the GraphQL API.
    """

    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            atividade = Atividade.objects.get(pk=id)
            atividade.delete()
            return DeleteAtividadeMutation(success=True)
        except Atividade.DoesNotExist:
            return DeleteAtividadeMutation(success=False)


class Mutation(graphene.ObjectType):
    """
    The Mutation class represents all the queries that can perform
    server-side data changes.
    """

    create_cliente = CreateClienteMutation.Field()
    update_cliente = UpdateClienteMutation.Field()
    delete_cliente = DeleteClienteMutation.Field()

    create_projeto = CreateProjetoMutation.Field()
    update_projeto = UpdateProjetoMutation.Field()
    delete_projeto = DeleteProjetoMutation.Field()

    create_atividade = CreateAtividade.Field()
    update_atividade = UpdateAtividadeMutation.Field()
    delete_atividade = DeleteAtividadeMutation.Field()
