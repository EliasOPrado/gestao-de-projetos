import graphene
import json
from datetime import date
from decimal import Decimal
from core.models import Cliente, Projeto, Atividade
from core.graphql.queries import Query
from core.graphql.mutations import Mutation
from core.graphql.schema import schema
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from graphene_django.utils.testing import graphql_query


class TestGraphql(TestCase):

    def setUp(self):
        """Initial data"""
        self.url = "/api/graphql/"
        self.content_type = "application/json"
        self.cliente1 = Cliente(
            nome="cliente1", email="cliente1@email.com", telefone="+5511972345738"
        )
        self.cliente1.save()
        self.projeto1 = Projeto(
            nome="projeto1", descricao="Primeiro Projeto", cliente=self.cliente1
        )
        self.projeto1.save()
        self.atividade1 = Atividade(
            projeto=self.projeto1,
            descricao="Primeira Atividade",
            prazo=date(2024, 12, 31),
        )
        self.atividade1.save()

    def test_list_clientes(self):
        query = """
            query {
                allClientes  {
                    id
                    nome
                    email
                    telefone
                }
            }
        """
        response = self.client.post(
            self.url,
            json.dumps({"query": query}),
            content_type=self.content_type,
        )
        content = json.loads(response.content)["data"]
        self.assertIsNotNone(content["allClientes"])
        self.assertEqual(content["allClientes"][0]["nome"], self.cliente1.nome)
        self.assertEqual(content["allClientes"][0]["email"], self.cliente1.email)
        self.assertEqual(content["allClientes"][0]["telefone"], self.cliente1.telefone)

    def test_get_user_by_id(self):
        query = f"""
            query {{
                getCliente(id: {self.cliente1.id}) {{
                    id
                    nome
                    email
                    telefone
                }}
            }}
        """
        response = self.client.post(
            self.url,
            json.dumps({"query": query}),
            content_type=self.content_type
        )
        content = json.loads(response.content)["data"]
        self.assertIsNotNone(content["getCliente"])
        self.assertEqual(content["getCliente"]["id"], str(self.cliente1.id))
        self.assertEqual(content["getCliente"]["nome"], self.cliente1.nome)
        self.assertEqual(content["getCliente"]["email"], self.cliente1.email)
        self.assertEqual(content["getCliente"]["telefone"], self.cliente1.telefone)

    def test_get_projetos_by_cliente_id(self):
        query = f"""
            query {{
                getProjetosByClienteId(clienteId:{self.cliente1.id}){{
                    id
                    nome
                    descricao
                    atividades {{
                    id
                    }}
                }}
            }}
        """
        response = self.client.post(
            self.url,
            json.dumps({"query": query}),
            content_type=self.content_type,
        )
        content = json.loads(response.content)["data"]
        self.assertIsNotNone(content["getProjetosByClienteId"])
        self.assertEqual(content["getProjetosByClienteId"][0]["id"], str(self.projeto1.id))
        self.assertEqual(content["getProjetosByClienteId"][0]["nome"],self.projeto1.nome)
        self.assertEqual(content["getProjetosByClienteId"][0]["descricao"],self.projeto1.descricao)


    def test_update_cliente(self):
        query = f"""
            mutation {{
                updateCliente(id: {self.cliente1.id}, input: {{
                    nome: "New Name",
                    email: "newemail@example.com",
                    telefone: "+1234567890"
                    }}) {{
                        cliente {{
                        id
                        nome
                        email
                        telefone
                        }}
                    }}
                }}
            """
        response = self.client.post(
            self.url,
            json.dumps({"query": query}),
            content_type=self.content_type,
        )
        content = json.loads(response.content)["data"]
        self.assertIsNotNone(content["updateCliente"])
        self.assertNotEqual(content["updateCliente"]["cliente"]["nome"], self.cliente1.nome)
        self.assertNotEqual(content["updateCliente"]["cliente"]["email"], self.cliente1.email)
        self.assertNotEqual(content["updateCliente"]["cliente"]["telefone"], self.cliente1.telefone)