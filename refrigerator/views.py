from django.shortcuts import render
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, generics, status, filters

from .serializers import RefrigeratorSerializer, PhotoSerializer, SensorSerializer
from .models import Refrigerator, Photo, Sensor

import json

# # 냉장고 번호 유효성 검사 - 회원가입 후 냉장고 번호 유효한 번호인지 확인
# # 받는 값 : fridge_number
# # 만든이 : snchoi
# @api_view(['GET'])
# def FridgeNumberVerification(request):
#     fridge_number = request.GET.get('fridge_number')
#     queryset = Refrigerator.objects.get(fridge_number=fridge_number)
#     serializer = RefrigeratorSerializer(queryset, many=True)
#     return Response(serializer.data)


# 냉장고 번호 유효성 검사 - 회원가입 후 냉장고 번호 유효한 번호인지 확인(조회)
# 사용자 email을 냉장고 정보에 매핑(삽입)
# 받는 값 : email, fridge_number
# 만든이 : snchoi
@api_view(['PUT'])
def InsertUserInfoToFridge(request):
    params = request.data
    fridge_number = params['fridge_number']
    email = params['email']

    try:
        # 냉장고 번호가 존재하는 번호라면 
        exist = Refrigerator.objects.get(fridge_number=fridge_number)

        # 사용자 정보 저장
        refri_info = Refrigerator.objects.get(fridge_number=fridge_number)
        refri_info.email = email
        try:
            refri_info.save()
            return Response({"result":True}, status=status.HTTP_201_CREATED)
        except:
            return Response({"result":False}, status=status.HTTP_400_BAD_REQUEST)
    except:
        # 존재하지 않는 냉장고 정보라면 오류
        return Response({"result":False}, status=status.HTTP_404_NOT_FOUND)




# 외출 모드 ON OFF 변경
# 받는 값 : email, motion_sensor_on_off -> (1/0)
# 만든이 : snchoi
@api_view(['PUT'])
def GoingOutMode(request):
    params = request.data
    email = params['email']
    motion_sensor_on_off = params['motion_sensor_on_off']
    refri_info = Refrigerator.objects.get(email=email)
    refri_info.motion_sensor_on_off = motion_sensor_on_off
    try:
        refri_info.save()
        return Response({"result":True}, status=status.HTTP_201_CREATED)
    except:
        return Response({"result":False}, status=status.HTTP_400_BAD_REQUEST)