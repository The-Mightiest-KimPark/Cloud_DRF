from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, generics, status, filters

# Create your views here.
@api_view(['GET','POST'])
def HelloAPI(request):
    # 이미지 정보 받음
    param = request.data
    print('param : ', param)
    # img_url = param['url']
    # reg_date = param['reg_date']
    # reg_time = param['reg_time']

    # AI분석 결과

    # 결과 저장

    # 빅데이터 함수 호출

    # 상태 리턴
    return Response("hello world!", param)