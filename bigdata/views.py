from django.shortcuts import render
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, generics, status, filters
from .serializers import RecommRecipeSerializer, AllRecipeSerializer, AnswercountSerializer
from .models import AllRecipe, RecommRecipe, Answercount, IntentModel, Preprocess
from ai.models import Grocery
from user.models import UserInfo
import pymysql
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.metrics.pairwise import linear_kernel
import time
import requests
from django.core import serializers
import json
import random
from .import load


# AI 이미지 분석을 통한 결과 저장
# 받는 값 : email
# 만든이 : jr
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
    # grocery = ' '.join(set(grocery.split()))

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
        # tfidf_matrix = TfidfVectorizer().fit_transform(recipe_df['ingredient_name'][n * 10000:(n + 1) * 10000]).toarray()
        # tfidf_matrix = HashingVectorizer(n_features=300000).transform(recipe_df['ingredient_name'][n * 10000:(n + 1) * 10000])
        # 코사인유사도
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

        # 냉장고재료 idx=0 으로 고정
        idx = 0
        sim_scores = list(enumerate(cosine_sim[idx]))

        # 유사도에 따라 레시피 정렬
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # 유사도가 높은 30개 레시피 (0번은 자기자신)
        sim_scores = sim_scores[1:31]

        # 유사도가 높은 30개 레시피 (0번은 자기자신, 무한루프방지 30개)
        sim_scores = sim_scores[1:31]
        # 유사도 0.6이상만 추출하기
        # for s in range(len(sim_scores)):
        #     if sim_scores[s][1] < 0.6:
        #         sim_scores = sim_scores[0:s]
        #         break

        # 유사도가 0.6이상의 레시피 인덱스 추출
        food_indices = [i[0] + (n * 10000) for i in sim_scores]
        sim_scores_list = [i[1] for i in sim_scores]
        index_list = index_list + food_indices
        score_list = score_list + sim_scores_list

    print('10000단위로 유사도검사 후 병합')

    # 합쳐진 유사도 0.6이상의 레시피중 유사도가 가장 높은 레피시 인덱스 30개 추출
    sim_df = pd.DataFrame({'food_indices': index_list, 'sim_scores': score_list})
    sim_df.sort_values(by='sim_scores', ascending=False, inplace=True)
    print('유사도1위',sim_df['sim_scores'][0])
    print(recipe_df['ingredient_name'][0])
    high_score_indices = sim_df['food_indices'].values.tolist()[:30]
    print('합쳐진 유사도 0.6이상의 레시피중 유사도가 가장 높은 레피시 인덱스 30개 추출')

    # 인덱스를 활용하여 30개의 레시피를 조회수 순으로 재정렬 후 10개 추출
    # recomm_recipe = recipe_data.iloc[high_score_indices]
    recipe_data = AllRecipe.objects.filter(pk__in=high_score_indices)
    recomm_recipe = recipe_data
    recomm_recipe = recomm_recipe.order_by('-views')
    recomm_recipe = recomm_recipe[:10]
    print('recomm_recipe : ', recomm_recipe)
    # recomm_recipe.reset_index(drop=True, inplace=True)
    print('인덱스를 활용하여 30개의 레시피를 조회수 순으로 재정렬 후 10개 추출')
    print('type-recomm_recipe : ', type(recomm_recipe))
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
        if serializer.is_valid():
            serializer.save()
            print(time.time() - start)
        else:
            print(serializer.errors)
            return False
    return True


# 추천레시피 조회(list) 
# 받는 값 : email
# 만든이 : snchoi
@api_view(['GET'])
def RecommRecipeGet(request):
    email = request.GET.get('email')
    recom_recipe_queryset = RecommRecipe.objects.filter(email=email)
    serializers = RecommRecipeSerializer(recom_recipe_queryset, many=True)
    # # 빅데이터 함수 호출(삽입)
    # result = BdRecommRecipe(email)
    # print('result : ', result)
    # print('---------end--------')
    return Response(serializers.data)


# 목적에 맞는 추천 레시피 조회
# 받는 값 : email
# 만든이 : snchoi
@api_view(['GET'])
def RecommRecipePurposeGet(request):
    email = request.GET.get('email')
    print(email)
    # 목적 값 가져오기
    purpose = UserInfo.objects.get(email=email).purpose
    print(purpose)
    # 이메일과 목적에 맞는 추천레시피 조회
    recom_recipe_queryset = RecommRecipe.objects.filter(Q(email=email),Q(purpose=purpose))
    serializers = RecommRecipeSerializer(recom_recipe_queryset, many=True)
    return Response(serializers.data)


# 추천레시피 랜덤으로 하나만 조회
# 받는 값 : email
# 만든이 : snchoi
@api_view(['GET'])
def RecommRecipeGetOne(request):
    email = request.GET.get('email')
    recom_recipe_queryset = RecommRecipe.objects.filter(email=email)
    serializers = RecommRecipeSerializer(recom_recipe_queryset, many=True)
    length = len(serializers.data)
    random_num = random.randint(0, length - 1)
    print(random_num)
    return Response(serializers.data[random_num])


# 추천레시피 상세 보기
# 받는 값 : all_recipe_id
# 만든이 : snchoi
@api_view(['GET'])
def RecommRecipeDetail(request):
    all_recipe_id = request.GET.get('all_recipe_id')

    queryset = AllRecipe.objects.filter(id=all_recipe_id)
    serializers = AllRecipeSerializer(queryset, many=True)
    return Response(serializers.data[0])


# 음성 답변 검색
# 받는 값 : email
# 만든이 : jr
def AnswerGroceryCount(email, query):
    start = time.time()
    # 전처리 객체 생성 (load.py)
    # 의도 파악
    # intent = IntentModel(model_name='./bigdata/chatbot/intent_model_21.h5', proprocess=p)
    predict = load.pre_intent.intent.predict_class(query)
    intent_name = load.pre_intent.intent.labels[predict]
    print('시간1', time.time() - start)
    # 개체명 인식 (향후 추가 예정)
    # from models.ner.NerModel import NerModel
    # ner = NerModel(model_name='../models/ner/ner_model.h5', proprocess=p)
    # predicts = ner.predict(query)
    # ner_tags = ner.predict_tags(query)

    print("질문 : ", query)
    print("=" * 100)
    print("의도 파악 : ", intent_name)
    # print("개체명 인식 : ", predicts)
    # print("답변 검색에 필요한 NER 태그 : ", ner_tags)
    print("=" * 100)

    start3 = time.time()
    # 답변 검색
    answer = Answercount.objects.values_list('answer').filter(email=email, intent=intent_name)
    if not answer:
        answer = "현재 냉장고 속에 존재하지 않습니다."
    else:
        answer = answer[0][0]

    print("답변 : ", answer)
    print('시간3', time.time() - start3)
    print('총시간', time.time()-start)
    return answer


# 챗봇 재료 개수 답변 검색
# 받는 값 : query
# 만든이 : snchoi
@api_view(['GET'])
def AnswerCountGet(request):
    email = request.GET.get('email')
    query = request.GET.get('query')
    Answercount_queryset = Answercount.objects.all()
    serializers = AnswercountSerializer(Answercount_queryset, many=True)
    # 빅데이터 함수 호출(삽입)
    result = AnswerGroceryCount(email,query)
    print('result : ', result)
    print('---------end--------')
    return Response({"result":result})


# 챗봇 답변 저장
# 받는 값 : email
# 만든이 : jr
def SaveGroceryCount(email):
    start = time.time()
    # 현재 식재료 받아오기
    grocery_name = Grocery.objects.filter(email=email).values_list('name', 'count')
    print('grocery_name',grocery_name)
    now_grocery_dict = {}

    # 현재 식재료별 개수 dictionary 생성
    for grocery in grocery_name:
        # 향후 DB 저장 형식이 동일 식재료는 1행으로 저장될 경우 if문 삭제가능
        if grocery[0] in now_grocery_dict.keys():
            total_count = now_grocery_dict[grocery[0]] + grocery[1]
            now_grocery_dict.update({grocery[0]: total_count})
        else:
            now_grocery_dict.update({grocery[0]: grocery[1]})
    print('now_grocery_dict',now_grocery_dict)
    print('시간1', time.time()-start)

    start2 = time.time()
    # email, 의도, 재료개수 dict형식 list 생성
    answer_dict_list = []
    intent_list = list(now_grocery_dict.keys())
    count_list = list(now_grocery_dict.values())
    for i in range(len(now_grocery_dict)):
        answer_dict = {'email' : email, 'intent': intent_list[i] + '개수', 'answer': count_list[i]}
        answer_dict_list.append(answer_dict)

    # DB삭제
    answer_grocery_count = Answercount.objects.filter(email=email)
    answer_grocery_count.delete()
    print('시간2', time.time() - start2)
    start3 = time.time()

    for answer in answer_dict_list:
        # 데이터 저장
        serializer = AnswercountSerializer(data=answer)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
            return False
    print('시간3', time.time() - start3)
    print('최종시간', time.time() - start)
    return True

# 챗봇 답변 저장(list)
# 받는 값 : email
# 만든이 : snchoi
@api_view(['GET'])
def SaveCountGet(request):
    email = request.GET.get('email')
    Answercount_queryset = Answercount.objects.filter(email=email)
    serializers = AnswercountSerializer(Answercount_queryset, many=True)
    # 빅데이터 함수 호출(삽입)
    result = SaveGroceryCount(email)
    print('result : ', result)
    print('---------end--------')
    return Response(serializers.data)