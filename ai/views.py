from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, generics, status, filters
from .serializers import GrocerySerializer
from bigdata.views import BdRecommRecipe

# AI 이미지 분석을 통한 결과 저장
@api_view(['POST'])
def AiImgGrocery(request):
    # 이미지 정보 받음
    params = request.data
    print('params : ', params)
    url = params['url']
    reg_date = params['reg_date']
    print(reg_date)
    fridge_number = params['fridge_number']

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
    BdRecommRecipe(data=ai_result, fridge_number= fridge_number)

    # 결과 저장
    for result in ai_result:
        result['fridge_number'] = fridge_number
        result['reg_date'] = reg_date
        result['gubun'] = 1

        serializer = GrocerySerializer(data=result)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)