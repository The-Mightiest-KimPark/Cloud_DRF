from django.shortcuts import render
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, generics, status, filters
from .serializers import GrocerySerializer, AllGrocerySerializer
from refrigerator.serializers import PhotoSerializer
from .models import Refrigerator, Photo, Sensor
from bigdata.views import BdRecommRecipe
from refrigerator.models import Refrigerator
import json

# 전체 냉장고 번호만 조회 - 회원가입 후 냉장고 번호 유효한 번호인지 확인
# 만든이 : snchoi
class FridgeNumberGet(generics.ListCreateAPIView):
    pass



# 사용자 email 냉장고 정보에 매핑(삽입)
# 만든이 : snchoi
@api_view(['GET','POST'])
def InsertUserInfoToFridge(request):
    pass


# 외출 모드ON OFF 변경
class GoingOutMode(generics.ListCreateAPIView):
    pass