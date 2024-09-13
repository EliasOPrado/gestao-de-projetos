from rest_framework import serializers
from core.models import Cliente, Atividade, Projeto


class ClienteModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cliente
        fields = '__all__'


class AtividadeModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Atividade
        fields = '__all__'


class ProjetoModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projeto
        fields = '__all__'
        