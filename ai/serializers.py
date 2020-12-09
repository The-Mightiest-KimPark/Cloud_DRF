from rest_framework import serializers
from .models import Grocery, AllGrocery

# 현제 식료품
class GrocerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Grocery
        fields= '__all__'

# 전체 식료품
class AllGrocerySerializer(serializers.ModelSerializer):
    class Meta:
        model = AllGrocery
        fields = '__all__'