import json
from datetime import datetime, date
from core.models import Cliente, Projeto, Atividade
from core.graphql.schema import schema
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist


class TestGraphql(TestCase):
    """
    Django TestCase.

    This class comes with different functionalities to mimics client
    requests and asserts.
    """

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

    def get_object_or_none(self, model_class, **kwargs):
        # Checks if a specific object exists or returns None
        try:
            return model_class.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    def test_all_clientes(self):
        # Test if returns all clientes
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

    def test_get_cliente_by_id(self):
        # Test if is possible get cliente by id
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
            self.url, json.dumps({"query": query}), content_type=self.content_type
        )
        content = json.loads(response.content)["data"]
        self.assertIsNotNone(content["getCliente"])
        self.assertEqual(content["getCliente"]["id"], str(self.cliente1.id))
        self.assertEqual(content["getCliente"]["nome"], self.cliente1.nome)
        self.assertEqual(content["getCliente"]["email"], self.cliente1.email)
        self.assertEqual(content["getCliente"]["telefone"], self.cliente1.telefone)

    def test_get_projetos_by_cliente_id(self):
        # Test get projetos by cliente id
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
        self.assertEqual(
            content["getProjetosByClienteId"][0]["id"], str(self.projeto1.id)
        )
        self.assertEqual(
            content["getProjetosByClienteId"][0]["nome"], self.projeto1.nome
        )
        self.assertEqual(
            content["getProjetosByClienteId"][0]["descricao"], self.projeto1.descricao
        )

    def test_create_cliente(self):
        # Test creating a cliente 
        query = """
            mutation {
                createCliente(input: {
                    nome: "New Name",
                    email: "newemail@example.com",
                    telefone: "+1234567890"
                }) {
                    cliente {
                    id
                    nome
                    email
                    telefone
                    }
                }
                }
            """
        response = self.client.post(
            self.url,
            json.dumps({"query": query}),
            content_type=self.content_type,
        )
        content = json.loads(response.content)["data"]
        self.assertIsNotNone(content["createCliente"])
        self.assertEqual(content["createCliente"]["cliente"]["nome"], "New Name")
        self.assertEqual(content["createCliente"]["cliente"]["telefone"], "+1234567890")
        self.assertEqual(
            content["createCliente"]["cliente"]["email"], "newemail@example.com"
        )

    def test_update_cliente(self):
        # Test updating a cliente
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
        self.assertNotEqual(
            content["updateCliente"]["cliente"]["nome"], self.cliente1.nome
        )
        self.assertNotEqual(
            content["updateCliente"]["cliente"]["email"], self.cliente1.email
        )
        self.assertNotEqual(
            content["updateCliente"]["cliente"]["telefone"], self.cliente1.telefone
        )

    def test_delete_cliente(self):
        # Test deleting a cliente
        query = f"""
            mutation {{
                deleteCliente(id: {self.cliente1.id}) {{
                    success
                }}
            }}
        """
        response = self.client.post(
            self.url,
            json.dumps({"query": query}),
            content_type=self.content_type,
        )
        content = json.loads(response.content)["data"]
        check_deleted_cliente = self.get_object_or_none(Cliente, id=self.cliente1.id)
        self.assertEqual(check_deleted_cliente, None)
        self.assertIsNotNone(content["deleteCliente"])
        self.assertEqual(content["deleteCliente"]["success"], True)

    def test_all_projetos(self):
        # Test if all projects are being returned
        query = """
            query {
                allProjetos{
                    id
                    nome
                    descricao
                    status
                    atividades {
                    id
                    }
                    cliente{
                    id
                    }
                }
            }
        """
        response = self.client.post(
            self.url,
            json.dumps({"query": query}),
            content_type=self.content_type,
        )
        content = json.loads(response.content)["data"]
        self.assertIsNotNone(content["allProjetos"])
        self.assertEqual(content["allProjetos"][0]["nome"], self.projeto1.nome)
        self.assertEqual(
            content["allProjetos"][0]["descricao"], self.projeto1.descricao
        )
        self.assertEqual(
            str.lower(content["allProjetos"][0]["status"]), self.projeto1.status
        )
        self.assertEqual(
            content["allProjetos"][0]["cliente"]["id"], str(self.cliente1.id)
        )
        self.assertEqual(
            content["allProjetos"][0]["atividades"][0]["id"], str(self.atividade1.id)
        )

    def test_get_atividades_by_projeto_id(self):
        # Test get atividade by projeto id
        query = f"""
            query {{
                getAtividadesByProjetoId(projetoId: {self.projeto1.id}) {{
                    id
                    descricao
                    dataCriacao
                    prazo
                    projeto {{
                        id
                        nome
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
        self.assertIsNotNone(content["getAtividadesByProjetoId"])
        self.assertEqual(
            content["getAtividadesByProjetoId"][0]["id"], str(self.atividade1.id)
        )
        self.assertEqual(
            content["getAtividadesByProjetoId"][0]["descricao"],
            self.atividade1.descricao,
        )
        self.assertEqual(
            datetime.fromisoformat(
                content["getAtividadesByProjetoId"][0]["dataCriacao"]
            ),
            self.atividade1.data_criacao,
        )
        self.assertEqual(
            content["getAtividadesByProjetoId"][0]["prazo"],
            self.atividade1.prazo.strftime("%Y-%m-%d"),
        )
        self.assertEqual(
            content["getAtividadesByProjetoId"][0]["projeto"]["id"],
            str(self.projeto1.id),
        )

    def test_create_projeto(self):
        # Test creating a projeto
        query = f"""
                mutation {{
                    createProjeto(input: {{
                        nome: "New Name",
                        descricao: "New description",  
                        status: "em_andamento",       
                        clienteId: "{self.cliente1.id}"  
                    }}) {{
                        projeto {{
                            id
                            nome
                            descricao
                            status
                            cliente {{
                                id
                                nome
                            }}
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
        self.assertIsNotNone(content["createProjeto"])
        self.assertEqual(content["createProjeto"]["projeto"]["nome"], "New Name")
        self.assertEqual(
            content["createProjeto"]["projeto"]["descricao"], "New description"
        )
        self.assertEqual(
            str.lower(content["createProjeto"]["projeto"]["status"]), "em_andamento"
        )

    def test_update_projeto(self):
        # Test updating a projeto
        query = f"""
            mutation {{
                updateProjeto(id: {self.projeto1.id}, input: {{
                    nome: "Update Project",
                    descricao: "Update Project description",
                    status: "concluido",
                    clienteId: {self.cliente1.id}
                        }}) {{
                            projeto {{
                            id
                            nome
                            descricao
                            status
                            cliente {{
                                id
                                nome
                            }}
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
        self.assertIsNotNone(content["updateProjeto"])
        self.assertEqual(content["updateProjeto"]["projeto"]["nome"], "Update Project")
        self.assertEqual(
            content["updateProjeto"]["projeto"]["descricao"],
            "Update Project description",
        )
        self.assertEqual(
            str.lower(content["updateProjeto"]["projeto"]["status"]), "concluido"
        )
        self.assertNotEqual(
            content["updateProjeto"]["projeto"]["nome"], self.projeto1.nome
        )
        self.assertNotEqual(
            content["updateProjeto"]["projeto"]["descricao"], self.projeto1.descricao
        )
        self.assertNotEqual(
            str.lower(content["updateProjeto"]["projeto"]["status"]),
            self.projeto1.status,
        )

    def test_delete_projeto(self):
        # Test deleting a projeto
        query = f"""
            mutation {{
                deleteProjeto(id: {self.projeto1.id}) {{
                    success
                }}
            }}
        """
        response = self.client.post(
            self.url,
            json.dumps({"query": query}),
            content_type=self.content_type,
        )
        content = json.loads(response.content)["data"]
        check_deleted_projeto = self.get_object_or_none(Projeto, id=self.projeto1.id)
        self.assertEqual(check_deleted_projeto, None)
        self.assertIsNotNone(content["deleteProjeto"])
        self.assertEqual(content["deleteProjeto"]["success"], True)

    def test_all_atividades(self):
        # Test returning all atividades
        query = """
            query {
                allAtividades{
                    id
                    descricao
                    dataCriacao
                    prazo
                    projeto {
                        id
                        nome
                        descricao
                        cliente{
                            id  
                        }
                    }
                }
            }
        """
        response = self.client.post(
            self.url,
            json.dumps({"query": query}),
            content_type=self.content_type,
        )
        content = json.loads(response.content)["data"]
        self.assertIsNotNone(content["allAtividades"])
        self.assertEqual(
            content["allAtividades"][0]["descricao"], self.atividade1.descricao
        )
        self.assertEqual(
            datetime.fromisoformat(content["allAtividades"][0]["dataCriacao"]),
            self.atividade1.data_criacao,
        )
        self.assertEqual(
            content["allAtividades"][0]["prazo"],
            self.atividade1.prazo.strftime("%Y-%m-%d"),
        )

    def test_get_atividades_by_projeto_id(self):
        # Test get atividades by projeto id
        query = f"""
            query {{
                getAtividadesByProjetoId(projetoId:{self.projeto1.id}){{
                    id
                    descricao
                    dataCriacao
                    prazo
                }}
            }}
        """
        response = self.client.post(
            self.url,
            json.dumps({"query": query}),
            content_type=self.content_type,
        )
        content = json.loads(response.content)["data"]
        self.assertIsNotNone(content["getAtividadesByProjetoId"])
        self.assertEqual(
            content["getAtividadesByProjetoId"][0]["descricao"],
            self.atividade1.descricao,
        )
        self.assertEqual(
            datetime.fromisoformat(
                content["getAtividadesByProjetoId"][0]["dataCriacao"]
            ),
            self.atividade1.data_criacao,
        )
        self.assertEqual(
            content["getAtividadesByProjetoId"][0]["prazo"],
            self.atividade1.prazo.strftime("%Y-%m-%d"),
        )

    def test_create_atividade(self):
        # Test creating atividade
        query = f"""
                mutation {{
                    createAtividade(input: {{
                        descricao: "New description",  
                        prazo: "2024-12-01"  
                        projetoId: "{self.projeto1.id}"  
                        }}) {{
                        atividade {{
                            id
                            descricao
                            prazo
                            dataCriacao
                            projeto {{
                                id
                                nome
                            }}
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
        self.assertIsNotNone(content["createAtividade"])
        self.assertEqual(
            content["createAtividade"]["atividade"]["descricao"], "New description"
        )
        self.assertEqual(content["createAtividade"]["atividade"]["prazo"], "2024-12-01")

    def test_update_atividade(self):
        # Test updating atividade
        query = f"""
            mutation {{
                updateAtividade(id: {self.atividade1.id}, input: {{
                    descricao: "Updated description",
                    prazo: "2024-12-02" 
                    projetoId: "{self.projeto1.id}"  
                    }}) {{
                        atividade {{
                            id
                            descricao
                            prazo
                            dataCriacao
                            projeto {{
                                id
                                nome
                            }}
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
        self.assertIsNotNone(content["updateAtividade"])
        self.assertNotEqual(
            content["updateAtividade"]["atividade"]["descricao"],
            self.atividade1.descricao,
        )
        self.assertNotEqual(
            content["updateAtividade"]["atividade"]["prazo"],
            self.atividade1.prazo.strftime("%Y-%m-%d"),
        )

    def test_delete_atividade(self):
        # Test deleting atividade
        query = f"""
            mutation {{
                deleteAtividade(id: {self.atividade1.id}) {{
                    success
                }}
            }}
        """
        response = self.client.post(
            self.url,
            json.dumps({"query": query}),
            content_type=self.content_type,
        )
        content = json.loads(response.content)["data"]
        check_deleted_atividade = self.get_object_or_none(
            Atividade, id=self.atividade1.id
        )
        self.assertEqual(check_deleted_atividade, None)
        self.assertIsNotNone(content["deleteAtividade"])
        self.assertEqual(content["deleteAtividade"]["success"], True)
