from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, generics, status, filters
from .serializers import RecommRecipeSerializer

# AI 이미지 분석을 통한 결과 저장
def BdRecommRecipe(data, fridge_number):
    print('hello world', data, fridge_number)
    # 재료 정보 받음 data = 재료정보, fridge_number = 냉장고 정보

    # 빅데이터 로직

    # 추천 레시피 결과 저장
