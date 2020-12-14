from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, generics, status, filters
from .serializers import RecommRecipeSerializer
import pymysql
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# AI 이미지 분석을 통한 결과 저장
def BdRecommRecipe(data, email):
    print('hello world', data, email)
    # 재료 정보 받음 data = 재료정보, email = 사용자id
    now_grocery = ' '.join(data['name'].values)

    # 빅데이터 로직
    # MariaDB에서 data호출
    conn = pymysql.connect(host='multi-bigdata.cljkqcsbb9ok.ap-northeast-2.rds.amazonaws.com', port=3306, user='edu12',
                           passwd='edu12', db='edudb04', cursorclass=pymysql.cursors.DictCursor)
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
    for n in range((len(data) // 10000) + 1):
        recipe_data.iloc[n*10000] = ['now_grocery', 0, now_grocery, 0, 0, 0, 0, 0,0]

    index_list = []
    score_list = []

    # tfidf벡터 생성
    tfidf = TfidfVectorizer()

    # 10000단위로 유사도검사 후 병합
    for n in range((len(data) // 10000) + 1):
        tfidf_matrix = tfidf.fit_transform(data['ingredient_name'][n * 10000:(n + 1) * 10000])

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

    # 인덱스를 활용하여 30개의 레시피를 조회수 순으로 재정렬
    recomm_recipe = data.iloc[high_score_indices]
    recomm_recipe.sort_values(by='views', ascending=False, inplace=True)
    recomm_recipe = recomm_recipe[:10]

    # 추천 레시피 결과 저장
