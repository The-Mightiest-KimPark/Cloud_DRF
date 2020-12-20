from rest_framework import serializers
from .models import RecommRecipe, AllRecipe, Answercount


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

# 추천 레시피
class AnswercountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answercount
        fields= '__all__'