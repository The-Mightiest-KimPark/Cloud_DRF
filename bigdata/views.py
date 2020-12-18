from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, generics, status, filters
from .serializers import RecommRecipeSerializer
from .models import AllRecipe, RecommRecipe
from ai.models import Grocery
import pymysql
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import time
import requests
from django.core import serializers
import json
import random


# AI 이미지 분석을 통한 결과 저장
# @api_view(['GET'])
def BdRecommRecipe(email):
    # email = request.GET.get('email')
    # print('빅데이터 진입')
    # 해당 사용자가 가지고 있는 재료정보
    # names = Grocery.objects.filter(email=email).only('name')
    names = Grocery.objects.all().only('name')
    # print('names',names)
    grocery = ''
    for name in list(names)[0:]:
        grocery = str(name) + ' ' + grocery
    # print('grocery',grocery)

    # 빅데이터 로직
    # MariaDB에서 data호출
    # recipe_data = AllRecipe.objects.values_list('id', 'name', 'ingredient', 'ingredient_name', 'seasoning', 'seasoning_name', 'howto', 'purpose', 'views', 'img', 'recipe_num')
    start = time.time()
    result = AllRecipe.objects.values_list('ingredient_name', 'views')

    recipe_df = pd.DataFrame(list(result), columns=['ingredient_name', 'views'])
    print(time.time() - start)
    # recipe_data = pd.DataFrame(list(result), columns=['id', 'name', 'ingredient', 'ingredient_name', 'seasoning', 'seasoning_name', 'howto', 'purpose', 'views', 'img', 'recipe_num'])
    # #print('빅데이터 로직')

    # # 현재 냉장고재료 0열에 추가
    for n in range((len(recipe_df) // 10000) + 1):
        recipe_df.iloc[n * 10000] = [grocery, 0]

    index_list = []
    score_list = []
    # print('현재 냉장고재료 0열에 추가')

    # tfidf벡터 생성
    tfidf = TfidfVectorizer()
    print('tfidf벡터 생성')

    # 10000단위로 유사도검사 후 병합
    for n in range((len(recipe_df) // 10000) + 1):
        tfidf_matrix = tfidf.fit_transform(recipe_df['ingredient_name'][n * 10000:(n + 1) * 10000])

        # 코사인유사도
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

        # 냉장고재료 idx=0 으로 고정
        idx = 0
        sim_scores = list(enumerate(cosine_sim[idx]))

        # 유사도에 따라 레시피 정렬
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # 유사도가 높은 30개 레시피 (0번은 자기자신)
        sim_scores = sim_scores[1:31]

        # 유사도가 높은 30개의 레시피 인덱스 추출
        food_indices = [i[0] + (n * 10000) for i in sim_scores]
        sim_scores_list = [i[1] for i in sim_scores]
        index_list = index_list + food_indices
        score_list = score_list + sim_scores_list

    print('10000단위로 유사도검사 후 병합')

    # 330개의 레시피중 유사도가 높은 레피시 인덱스 30개 추출
    sim_df = pd.DataFrame({'food_indices': index_list, 'sim_scores': score_list})
    sim_df.sort_values(by='sim_scores', ascending=False, inplace=True)
    high_score_indices = sim_df['food_indices'].values.tolist()[:30]
    print('330개의 레시피중 유사도가 높은 레피시 인덱스 30개 추출')

    # 인덱스를 활용하여 30개의 레시피를 조회수 순으로 재정렬 후 10개 추출
    # recomm_recipe = recipe_data.iloc[high_score_indices]
    recipe_data = AllRecipe.objects.filter(pk__in=high_score_indices)
    recomm_recipe = recipe_data
    recomm_recipe = recomm_recipe.order_by('-views')
    recomm_recipe = recomm_recipe[:10]
    print('recomm_recipe : ', recomm_recipe)
    # recomm_recipe.reset_index(drop=True, inplace=True)
    print('인덱스를 활용하여 30개의 레시피를 조회수 순으로 재정렬 후 10개 추출')

    # json으로 변환
    recomm_recipe_to_json = serializers.serialize("json", recomm_recipe)
    recomm_recipe_results = json.loads(recomm_recipe_to_json)
    print('json으로 변환')
    print('recomm_recipe_resultsm : ', recomm_recipe_results)
    # print('type : ', type(recomm_recipe_results))

    # 해당 사용자의 이전 결과 다 삭제
    recommRecipe = RecommRecipe.objects.filter(email=email)
    if recommRecipe:
        recommRecipe.delete()
        # print('삭제완료')
    # print('해당 사용자의 이전 결과 다 삭제')

    # 사용자 이메일 컬럼 추가
    for recomm_recipe_result in recomm_recipe_results:
        body = recomm_recipe_result['fields']
        print(body)
        body['email'] = email
        body['all_recipe_id'] = recomm_recipe_result['pk']
        # print('recomm_recipe_result : ', recomm_recipe_result)
        # 데이터 저장
        serializer = RecommRecipeSerializer(data=body)
        print(time.time() - start)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
            return False
    return True


# 추천레시피 조회
# 받는 값 : email
@api_view(['GET'])
def RecommRecipeGet(request):
    email = request.GET.get('email')
    recom_recipe_queryset = RecommRecipe.objects.filter(email=email)
    serializers = RecommRecipeSerializer(recom_recipe_queryset, many=True)
    # 빅데이터 함수 호출(삽입)
    result = BdRecommRecipe(email)
    print('result : ', result)
    print('---------end--------')
    return Response(serializers.data)


# 추천레시피 랜덤으로 하나만 조회
# 받는 값 : email
@api_view(['GET'])
def RecommRecipeGetOne(request):
    email = request.GET.get('email')
    recom_recipe_queryset = RecommRecipe.objects.filter(email=email)
    serializers = RecommRecipeSerializer(recom_recipe_queryset, many=True)
    length = len(serializers.data)
    random_num = random.randint(0, length - 1)
    print(random_num)
    return Response(serializers.data[random_num])

