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

import requests
import json

# AI 이미지 분석을 통한 결과 저장
@api_view(['GET'])
def BdRecommRecipe(request):
    email = request.GET.get('email')

    # 해당 사용자가 가지고 있는 재료정보 
    response = requests.get(f'http://3.92.44.79/api/user-input-grocery/?email={email}')
    data = response.text
    grocery = re.findall('"name":".*?"', data)
    grocery = ' '.join(grocery)
    grocery = re.sub('[",:,name]', '', grocery)

    # 빅데이터 로직
    # MariaDB에서 data호출
    result = AllRecipe.objects.values_list('id', 'name', 'ingredient', 'ingredient_name', 'seasoning', 'seasoning_name', 'howto', 'purpose', 'views', 'img', 'recipe_num')

    recipe_data = pd.DataFrame(list(result), columns=['id', 'name', 'ingredient', 'ingredient_name', 'seasoning', 'seasoning_name', 'howto', 'purpose', 'views', 'img', 'recipe_num'])

    # 현재 냉장고재료 0열에 추가
    for n in range((len(recipe_data) // 10000) + 1):
        recipe_data.iloc[n * 10000] = [n * 10000, 'grocery', 0, grocery, 0, 0, 0, 0, 0, 0, 0]

    index_list = []
    score_list = []

    # tfidf벡터 생성
    tfidf = TfidfVectorizer()

    # 10000단위로 유사도검사 후 병합
    for n in range((len(recipe_data) // 10000) + 1):
        tfidf_matrix = tfidf.fit_transform(recipe_data['ingredient_name'][n * 10000:(n + 1) * 10000])

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

    # 330개의 레시피중 유사도가 높은 레피시 인덱스 30개 추출
    sim_df = pd.DataFrame({'food_indices': index_list, 'sim_scores': score_list})
    sim_df.sort_values(by='sim_scores', ascending=False, inplace=True)
    high_score_indices = sim_df['food_indices'].values.tolist()[:30]

    # 인덱스를 활용하여 30개의 레시피를 조회수 순으로 재정렬 후 10개 추출
    recomm_recipe = recipe_data.iloc[high_score_indices]
    recomm_recipe.sort_values(by='views', ascending=False, inplace=True)
    recomm_recipe = recomm_recipe[:10]
    recomm_recipe.reset_index(drop=True, inplace=True)

    # json으로 변환
    recomm_recipe_to_json = recomm_recipe.to_json(orient="records")
    recomm_recipe_results = json.loads(recomm_recipe_to_json)
    
    # 해당 사용자의 이전 결과 다 삭제
    recommRecipe = RecommRecipe.objects.filter(email=email)
    if recommRecipe:
        recommRecipe.delete()

    # 사용자 이메일 컬럼 추가
    for recomm_recipe_result in recomm_recipe_results:
        recomm_recipe_result['email'] = email
        recomm_recipe_result['all_recipe_id'] = recomm_recipe_result['id']

        # 데이터 저장
        serializer = RecommRecipeSerializer(data=recomm_recipe_result)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

