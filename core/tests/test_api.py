from datetime import date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Cliente, Projeto, Atividade


class TestApi(APITestCase):

    def setUp(self):
        """Initial data"""
        self.headerInfo = {"content-type": "application/json"}
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

        # payloads
        self.cliente_data = {
            "nome": "Joao 123",
            "email": "joao123@email.com",
            "telefone": "+551198048399",
        }

        self.projeto_data = {
            "nome": "projeto2",
            "descricao": "Segundo Projeto",
            "cliente": self.cliente1.id,
        }

        self.atividade_data = {
            "projeto": self.projeto1.id,
            "descricao": "Segunda descricao",
            "prazo": date(2024, 12, 31),
        }

        # urls
        self.cliente_list = reverse("core:clientes-list")
        self.cliente_detail = reverse(
            "core:clientes-detail", kwargs={"pk": self.cliente1.id}
        )

        self.projeto_list = reverse("core:projetos-list")
        self.projeto_detail = reverse(
            "core:projetos-detail", kwargs={"pk": self.projeto1.id}
        )

        self.atividade_list = reverse("core:atividades-list")
        self.atividade_detail = reverse(
            "core:atividades-detail", kwargs={"pk": self.atividade1.id}
        )

    def test_get_cliente(self):
        """Test if GET request is returning 200"""
        response = self.client.get(self.cliente_list, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_cliente(self):
        """Test if POST request is returning 201"""
        response = self.client.post(self.cliente_list, self.cliente_data, format="json")
        self.assertTrue(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_cliente_with_wrong_telefone(self):
        """Test if POST requirest is returning 400"""
        data = {
            "nome": "Joao 123",
            "email": "joao123@email.com",
            "telefone": "ABCDEF",
        }
        response = self.client.post(self.cliente_list, data, format="json")
        response_data = response.json()
        self.assertEqual(
            response_data["telefone"][0],
            "Phone number must be entered in the format: '+999999999'. Up to 20 digits allowed.",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_cliente(self):
        """Test if UPDATE is returning 200 and data is updated."""
        data = {
            "nome": "Joao 123 UPDATED",
            "email": "new_joao123@email.com",
            "telefone": "+551198048388",
        }
        response = self.client.put(
            self.cliente_detail, data, format="json", headers=self.headerInfo
        )
        self.assertNotEqual(self.cliente_data, data)
        self.assertNotEqual(self.cliente1.nome, data["nome"])
        self.assertNotEqual(self.cliente1.email, data["email"])
        self.assertNotEqual(self.cliente1.telefone, data["telefone"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_cliente(self):
        """Test if DELETE is returning 204 and data is deleted."""
        response = self.client.delete(
            self.cliente_detail, format="json", headers=self.headerInfo
        )

        self.assertFalse(response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # --- Projeto ---
    def test_get_projeto(self):
        """Test if GET request is returning 200"""
        response = self.client.get(self.projeto_list, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_projeto(self):
        """Test if POST request is returning 201"""
        response = self.client.post(self.projeto_list, self.projeto_data, format="json")
        self.assertTrue(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_projeto(self):
        """Test if UPDATE is returning 200 and data is updated."""
        data = {
            "nome": "projeto2 UPDATED",
            "descricao": "Segundo Projeto UPDATED",
            "cliente": self.cliente1.id,
        }
        response = self.client.put(
            self.projeto_detail, data, format="json", headers=self.headerInfo
        )
        self.assertNotEqual(self.projeto_data, data)
        self.assertNotEqual(self.projeto1.nome, data["nome"])
        self.assertNotEqual(self.projeto1.descricao, data["descricao"])
        self.assertEqual(self.cliente1.id, data["cliente"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_projeto(self):
        """Test if DELETE is returning 204 and data is deleted."""
        response = self.client.delete(
            self.projeto_detail, format="json", headers=self.headerInfo
        )

        self.assertFalse(response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # --- Atividade ---
    def test_get_atividade(self):
        """Test if GET request is returning 200"""
        response = self.client.get(self.atividade_list, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_atividade(self):
        """Test if POST request is returning 201"""
        response = self.client.post(
            self.atividade_list, self.atividade_data, format="json"
        )
        self.assertTrue(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_atividade(self):
        """Test if UPDATE is returning 200 and data is updated."""
        data = {
            "projeto": self.projeto1.id,
            "descricao": "Segunda descricao UPDATED",
            "prazo": date(2024, 12, 28),
        }
        response = self.client.put(
            self.atividade_detail, data, format="json", headers=self.headerInfo
        )
        self.assertNotEqual(self.atividade_data, data)
        self.assertEqual(self.atividade1.projeto.id, data["projeto"])
        self.assertNotEqual(self.atividade1.descricao, data["descricao"])
        self.assertNotEqual(self.atividade1.prazo, data["prazo"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_atividade(self):
        """Test if DELETE is returning 204 and data is deleted."""
        response = self.client.delete(
            self.atividade_detail, format="json", headers=self.headerInfo
        )

        self.assertFalse(response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
