from django.shortcuts import render
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, generics, status, filters

from .serializers import GrocerySerializer, AllGrocerySerializer
from refrigerator.serializers import PhotoSerializer
from refrigerator.models import Photo
from .models import Grocery, AllGrocery
from bigdata.views import BdRecommRecipe
from refrigerator.models import Refrigerator
from ai.my_yolo import YOLO
from urllib import request as rqt
from io import BytesIO
from PIL import Image
from pytz import timezone
import json
import datetime
#import boto3
import awskey
# import s3fs
import requests


# from django.utils import timezone

# AI 이미지 분석을 통한 결과 저장
# 만든이 : snchoi
@api_view(['GET'])
def AiImgGrocery(request):
    # # 이미지 정보 받음
    # params = request.data
    # url = params['url']
    # reg_date = params['reg_date']
    # fridge_number = params['fridge_number']
    #
    # # 냉장고 번호를 통해 아이디 값 가져오기
    # refri = Refrigerator.objects.get(fridge_number=fridge_number)
    # email = refri.email
    # print('email : ', email)
    #
    # # 이미지 저장
    # serializer = PhotoSerializer(data={"email":email,"file_name":fridge_number,"url":url,"reg_date":reg_date})
    # if serializer.is_valid():
    #     serializer.save()
    #     print('이미지 저장 성공')
    # else:
    #     print('이미지 저장 실패')
    #------------근웅----------------

    url = "https://themightiestkpk1.s3.amazonaws.com/train12124.jpg"
    model_path = 'ai/000/trained_weights_final.h5'
    class_path = 'ai/_classes.txt'

    yolo = YOLO(model_path=model_path, classes_path=class_path)

    # 이미지 로딩
    res = rqt.urlopen(url).read()
    img = Image.open(BytesIO(res))
    ai_result = yolo.my_detect_image(img)

    # ------------------------------



    # 빅데이터 함수 호출(냉장고 번호와 재료들 넘겨줘야함?)
    # BdRecommRecipe(data=ai_result, email= email)
    #
    # # 결과 저장
    # for result in ai_result:
    #     result['email'] = email
    #     result['reg_date'] = reg_date
    #     result['gubun'] = 1

        # serializer = GrocerySerializer(data=result)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(ai_result)

  
# AI 이미지 분석을 통한 결과 저장 복사본
# 만든이 : snchoi
@api_view(['POST'])
def AiImgGroceryTest(request):
    # 이미지 정보 받음
    params = request.data
    url = params['url']
    reg_date = params['reg_date']
    fridge_number = params['fridge_number']

    # 냉장고 번호를 통해 아이디 값 가져오기
    refri = Refrigerator.objects.get(fridge_number=fridge_number)
    email = refri.email
    print('email : ', email)

    
    # 이전 날짜 이미지 다 삭제
    photo = Photo.objects.filter(email=email)
    if photo:
        photo.delete()
    
    # 이미지 저장
    serializer = PhotoSerializer(data={"email":email,"file_name":fridge_number,"url":url,"reg_date":reg_date})
    if serializer.is_valid():
        serializer.save()
        print('이미지 저장 성공')
    else:
        print('이미지 저장 실패')

    # AI분석 로직
    ai_result = [{
        'all_grocery_id': 1,
        'name' : '바나나',
        'count' : 3,
        'coordinate' : [[1,2],[3,2]]
    },{
        'all_grocery_id': 2,
        'name' : '사과',
        'count' : 1,
        'coordinate' : [[1,2],[3,2]]
    },{
        'all_grocery_id': 3,
        'name' : '고구마',
        'count' : 2,
        'coordinate' : [[1,2],[3,2]]
    }]

    # 이전 결과 다 삭제
    grocery = Grocery.objects.filter(email=email)
    if grocery:
        grocery.delete()
    
    # 결과 저장
    for result in ai_result:
        result['email'] = email
        result['reg_date'] = reg_date
        result['gubun'] = 1

        serializer = GrocerySerializer(data=result)
        if serializer.is_valid():
            try:
                serializer.save()
                print('이미지 인식 재료 결과 저장 완료')
            except:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 빅데이터 함수 호출
    # headers = {"Content-Type": "application/json"}
    # data = {"email":email}
    # res = requests.post('http://52.91.0.142:8000/api/bd-recomm-recipe/', data=data, headers=headers)
    BdRecommRecipe(email= email)

    return Response(serializer.data, status=status.HTTP_201_CREATED)



# 전체 재료 이름, 재료id 조회 - 직접 입력 시 존재하는 재료에서 선택하도록 
# 만든이 : snchoi
class AllGroceryName(generics.ListCreateAPIView):
    queryset = AllGrocery.objects.all()
    serializer_class = AllGrocerySerializer

# @api_view(['GET'])
# def test(request):

#     # s3 정보 가져오기
#     s3_client = boto3.client('s3',
#             region_name = awskey.AWS_REGION,
#             aws_access_key_id = awskey.AWS_ACCESS_KEY_ID,
#             aws_secret_access_key = awskey.AWS_SECRET_ACCESS_KEY)

#     s3_resource = boto3.resource('s3',
#             region_name = awskey.AWS_REGION,
#             aws_access_key_id = awskey.AWS_ACCESS_KEY_ID,
#             aws_secret_access_key = awskey.AWS_SECRET_ACCESS_KEY)

#     bucket_name = awskey.AWS_STORAGE_BUCKET_NAME
#     my_bucket = s3_resource.Bucket(bucket_name)
    
#     for file in my_bucket.objects.all():
#         params = {'Bucket': bucket_name, 'Key': file.key}
        
#         # 사진 URL
#         url = s3_client.generate_presigned_url('get_object', params)
#         print('url : ', url)

#         # 파일 이름
#         fridge_number = (file.key).split('.')[0]
#         print('fridge_number : ', fridge_number)

    
#     return Response({"result": True})

    # data = request.data
    # serializer = GrocerySerializer(data=data)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 가장 최근 재료 조회(gubun=1 : 이미지 인식 ,  gubun=2 : 직접입력) / 사용자 재료 입력
# 만든이 : snchoi
@api_view(['GET','POST', 'PUT', 'DELETE'])
def userInputGrocery(request):

    # 재료 조회(gubun=1 : 이미지 인식 ,  gubun=2 : 직접입력)
    if request.method == 'GET':
        gubun = request.GET.get('gubun')
        email = request.GET.get('email')

        # 구분값이 존재한다면 
        if gubun:
            queryset = Grocery.objects.filter(Q(gubun=gubun),Q(email=email))
        
        # 구분값이 존재하지 않는다면
        else:
            queryset = Grocery.objects.filter(Q(email=email))
            
        serializer = GrocerySerializer(queryset, many=True)
        return Response(serializer.data)
    
    # 사용자 재료 입력
    elif request.method == 'POST':
        data = request.data
        data['gubun'] = 2 #구분값은 직접입력 값인 2로 지정
        serializer = GrocerySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 사용자 입력 재료 수정
    elif request.method == 'PUT':
        data = request.data
        email = data['email']
        name = data['name']
        count = data['count']
        all_grocery_id = data['all_grocery_id']
        try:
            grocery_queryset = Grocery.objects.get(Q(all_grocery_id=all_grocery_id),Q(email=email),Q(gubun=2))
            grocery_queryset.name = name
            grocery_queryset.count = count
            grocery_queryset.all_grocery_id = data['all_grocery_id']

            try:
                grocery_queryset.save()
                return Response({"result":True}, status=status.HTTP_201_CREATED)
            except:
                return Response({"result":False}, status=status.HTTP_400_BAD_REQUEST)
        
        except:
            return Response({"result":False}, status=status.HTTP_404_NOT_FOUND)


    # 사용자 입력 재료 삭제
    elif request.method == 'DELETE':
        data = request.data
        email = data['email']
        all_grocery_id = data['all_grocery_id']
        try:
            queryset = Grocery.objects.get(Q(all_grocery_id=all_grocery_id),Q(email=email))
            queryset.delete()
        except:
            return Response({"result":False}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"result":True}, status=status.HTTP_201_CREATED)


        

