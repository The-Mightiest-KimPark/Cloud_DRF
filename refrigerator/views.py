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




# 외출모드 ON OFF 변경
# 받는 값 : email, outing_mode -> (1/0)
# 만든이 : snchoi
@api_view(['PUT'])
def GoingOutMode(request):
    params = request.data
    email = params['email']
    outing_mode = params['outing_mode']
    refri_info = Refrigerator.objects.get(email=email)
    refri_info.outing_mode = outing_mode
    try:
        refri_info.save()
        return Response({"result":True}, status=status.HTTP_201_CREATED)
    except:
        return Response({"result":False}, status=status.HTTP_400_BAD_REQUEST)


# 알림모드 ON OFF 변경
# 받는 값 : email, alarm_mode -> (1/0)
# 만든이 : snchoi
@api_view(['PUT'])
def AlarmMode(request):
    params = request.data
    email = params['email']
    alarm_mode = params['alarm_mode']
    refri_info = Refrigerator.objects.get(email=email)
    refri_info.alarm_mode = alarm_mode
    try:
        refri_info.save()
        return Response({"result":True}, status=status.HTTP_201_CREATED)
    except:
        return Response({"result":False}, status=status.HTTP_400_BAD_REQUEST)




# 센서값 조회
# 받는 값 : email. name(센서이름)
# 만든이 : snchoi
@api_view(['GET'])
def SensorValue(request):
    email = request.GET.get('email')
    print(email)
    name = request.GET.get('name')
    print(name)

    queryset = Sensor.objects.filter(Q(email=email),Q(name=name))
    serializer = SensorSerializer(queryset, many=True)
    return Response(serializer.data)


