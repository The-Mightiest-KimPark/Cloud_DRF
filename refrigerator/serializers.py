from rest_framework import serializers
from .models import Refrigerator, Photo, Seosor


# 냉장고
class RefrigeratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refrigerator
        fields= '__all__'

# 사진 
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields= '__all__'

# 센서
class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seosor
        fields= '__all__'