from rest_framework import serializers
from .models import RecommRecipe, AllRecipe


# 추천 레시피
class RecommRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommRecipe
        fields= '__all__'

# 전체 레시피
class AllRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllRecipe
        fields= '__all__'