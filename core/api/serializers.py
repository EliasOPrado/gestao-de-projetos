from rest_framework import serializers
from core.models import Cliente, Atividade, Projeto


class ClienteModelSerializer(serializers.ModelSerializer):
    """
    Django REST Framework ModelSerializer for the Cliente model.

    This class maps the Cliente Django model to a serializer, allowing it to
    be converted to and from JSON format.
    """

    class Meta:
        model = Cliente
        fields = "__all__"


class ProjetoModelSerializer(serializers.ModelSerializer):
    """
    Django REST Framework ModelSerializer for the Projeto model.

    This class maps the Projeto Django model to a serializer, allowing it to
    be converted to and from JSON format.
    """

    class Meta:
        model = Projeto
        fields = "__all__"


class AtividadeModelSerializer(serializers.ModelSerializer):
    """
    Django REST Framework ModelSerializer for the Atividade model.

    This class maps the Atividade Django model to a serializer, allowing it to
    be converted to and from JSON format.
    """

    class Meta:
        model = Atividade
        fields = "__all__"
