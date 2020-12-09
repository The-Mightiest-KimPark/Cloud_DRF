from django.shortcuts import render
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, generics, status, filters
from .serializers import GrocerySerializer, AllGroceryNameSerializer
from refrigerator.serializers import PhotoSerializer
from .models import Grocery, AllGrocery
from bigdata.views import BdRecommRecipe
from refrigerator.models import Refrigerator
import json

# AI 이미지 분석을 통한 결과 저장
# 만든이 : snchoi
@api_view(['POST'])
def AiImgGrocery(request):
    # 이미지 정보 받음
    params = request.data
    url = params['url']
    reg_date = params['reg_date']
    fridge_number = params['fridge_number']

    # 냉장고 번호를 통해 아이디 값 가져오기
    refri = Refrigerator.objects.get(fridge_number=fridge_number)
    email = refri.email
    print('email : ', email)

    # 이미지 저장
    serializer = PhotoSerializer(data={"email":email,"file_name":fridge_number,"url":url,"reg_date":reg_date})
    if serializer.is_valid():
        serializer.save()
        print('이미지 저장 성공')
    else:
        print('이미지 저장 실패')

    # AI분석 로직
    ai_result = [{
        'name' : '바나나',
        'count' : 3
    },{
        'name' : '사과',
        'count' : 1
    },{
        'name' : '고구마',
        'count' : 2
    }]

    # 빅데이터 함수 호출(냉장고 번호와 재료들 넘겨줘야함?)
    BdRecommRecipe(data=ai_result, email= email)

    # 결과 저장
    for result in ai_result:
        result['email'] = email
        result['reg_date'] = reg_date
        result['gubun'] = 1

        serializer = GrocerySerializer(data=result)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 전체 재료 이름 조회 - 직접 입력 시 존재하는 재료에서 선택하도록 
# 만든이 : snchoi
class AllGroceryName(generics.ListCreateAPIView):
    queryset = AllGrocery.objects.all().values('name')
    serializer_class = AllGroceryNameSerializer



# 가장 최근 재료 조회(gubun=1 : 이미지 인식 ,  gubun=2 : 직접입력) / 사용자 재료 입력
# 만든이 : snchoi
@api_view(['GET','POST'])
def userInputGrocery(request):
    gubun = request.GET.get('gubun')
    email = request.GET.get('email')

    if request.method == 'GET':
        #  {
        # 	"gubun": 1 또는 2, 
        # 	"email": "test2"
        # }
        latest_date = Grocery.objects.filter(Q(gubun=gubun),Q(email=email)).order_by('-reg_date')[:1].values_list('reg_date', flat=True)
        queryset = Grocery.objects.filter(Q(gubun=gubun),Q(email=email),Q(reg_date=latest_date))
        serializer = GrocerySerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # {
        # "email": "test",
        # "name": "banana",
        # "count": 3,
        # "reg_date": "2020-12-08T00:00:00Z"-현재날짜,
        # "gubun": "2"
        # }   
        serializer = GrocerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

