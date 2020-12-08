from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, generics, status, filters
from .serializers import GrocerySerializer

# AI 이미지 분석을 통한 결과 저장
@api_view(['GET','POST'])
def HelloAPI(request):
    # 이미지 정보 받음
    params = request.data
    url = params['url']
    reg_date = params['reg_date']
    reg_time = params['reg_time']
    refri_number = params['refri_number']

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

    # 결과 저장
    for result in ai_result:
        result['refri_number'] = refri_number
        result['reg_date'] = reg_date
        result['reg_time'] = reg_time
        result['gubun'] = 1

        serializer = GrocerySerializer(data=result)
        if serializer.is_valid():
            serializer.save()
            # 빅데이터 함수 호출(냉장고 번호와 재료들 넘겨줘야함?)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)