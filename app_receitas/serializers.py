# app_receitas/serializers.py
from rest_framework import serializers
from .models import Ingrediente, Receita

class IngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = ['id', 'nome']

class ReceitaSerializer(serializers.ModelSerializer):
    ingredientes = IngredienteSerializer(many=True, read_only=True) # Para exibir os ingredientes

    class Meta:
        model = Receita
        fields = ['id', 'nome', 'descricao', 'modo_preparo', 'tempo_preparo_minutos', 'ingredientes', 'imagem_url', 'link_externo']