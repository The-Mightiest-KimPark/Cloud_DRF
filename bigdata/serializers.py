from rest_framework import serializers
from .models import RecommRecipe

class RecommRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommRecipe
        fields= '__all__'