from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, generics, status, filters
from .serializers import RecommRecipeSerializer
from ai.models import Grocery
import pymysql
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

import requests

# AI 이미지 분석을 통한 결과 저장
@api_view(['POST'])
def BdRecommRecipe(request):
    print('빅데이터 진입')
    # 해당 사용자가 가지고 있는 재료정보 
    print('request : ', request.data)
    email = request.data['email']
    print('email : ', email)
    response = requests.get(f'http://127.0.0.1:8000/api/user-input-grocery/?email={email}')
    print('response : ', response.text)
    print('빅데이터 함수에서 여기까지 왔다')

    grocery = ' '.join(data['name'].values)

    # 빅데이터 로직
    # MariaDB에서 data호출
    conn = pymysql.connect(host='themightiestkpk.c9jl6xhdt5hy.us-east-1.rds.amazonaws.com', port=3306, user='admin',
                           passwd='themightiestkpk1', db='themightiestkpk', cursorclass=pymysql.cursors.DictCursor)
    try:
        cur = conn.cursor()
        sql = '''
            SELECT *
            FROM ALL_RECIPE
            WHERE 1 = 1
        '''
        cur.execute(sql)
        result = cur.fetchall()
    finally:
        conn.close()
    # 데이터프레임생성
    recipe_data = pd.DataFrame(result)

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

    # 추천 레시피 결과 저장
    for re_num in range(10):
        id_num = re_num + 1
        all_recipe_id = int(recomm_recipe['id'][re_num])
        name = recomm_recipe['name'][re_num]
        ingredient = recomm_recipe['ingredient'][re_num]
        ingredient_name = recomm_recipe['ingredient_name'][re_num]
        seasoning = recomm_recipe['seasoning'][re_num]
        seasoning_name = recomm_recipe['seasoning_name'][re_num]
        howto = recomm_recipe['howto'][re_num]
        purpose = recomm_recipe['purpose'][re_num]
        views = int(recomm_recipe['views'][re_num])
        img = recomm_recipe['img'][re_num]
        recipe_num = int(recomm_recipe['recipe_num'][re_num])

        # MariaDB에 저장
        conn = pymysql.connect(host='themightiestkpk.c9jl6xhdt5hy.us-east-1.rds.amazonaws.com', port=3306, user='admin',
                               passwd='themightiestkpk1', db='themightiestkpk', cursorclass=pymysql.cursors.DictCursor)
        try:
            cur = conn.cursor()
            #             sql = "INSERT INTO RECOMM_RECIPE VALUES (id, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            sql = "UPDATE RECOMM_RECIPE SET id=id, email=%s, all_recipe_id=%s, name=%s, ingredient=%s, ingredient_name=%s, seasoning=%s, seasoning_name=%s, howto=%s, purpose=%s, views=%s, img=%s, recipe_num=%s WHERE id=%s"
            val = (
            email, all_recipe_id, name, ingredient, ingredient_name, seasoning, seasoning_name, howto, purpose, views,
            img, recipe_num, id_num)
            cur.execute(sql, val)
        finally:
            conn.commit()
            conn.close()

