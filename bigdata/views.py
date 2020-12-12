from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, generics, status, filters
from .serializers import RecommRecipeSerializer

# AI 이미지 분석을 통한 결과 저장
def BdRecommRecipe(data, email):
    print('hello world', data, email)
    # 재료 정보 받음 data = 재료정보, email = 사용자id

    # 직접입력 재료까지 입력한 값 불러오기(가장 최근 날짜) - db에서 불러옴

    # 빅데이터 로직

    # 추천 레시피 결과 저장
