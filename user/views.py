from django.shortcuts import render
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, generics, status, filters
from .serializers import UserInfoSerializer, FollowSerializer, RecipeFavoriteSerializer
from .models import UserInfo, Follow, RecipeFavorite
from refrigerator.models import Photo
from refrigerator.serializers import PhotoSerializer
import json


# 팔로우 / 언팔로우 
# 받는 값(json) : email, following_user_id
# 만든이 : snchoi
@api_view(['PUT'])
def FollowAndUnfollow(request):
    params = request.data
    email = params['email']
    following_user_id = params['following_user_id']
    # 해당 id,email에 해당하는 값 존재 확인
    followTF = Follow.objects.filter(Q(email=email),Q(following_user_id=following_user_id))
    followTF = len(followTF)
    print('followTF : ', followTF)
    if followTF==0:
        # 존재하지 않을 경우 insert
        serializer = FollowSerializer(data=params)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        # 존재할 경우 delete
        result = Follow.objects.filter(Q(email=email),Q(following_user_id=following_user_id)).delete()
        if len(result):
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)



# 팔로우 된 상태일 때 친구 냉장고 가장최근 사진 조회 (조건: read안읽고, 최신사진순으로)
# 받는 값 : email
# 만든이 : snchoi
@api_view(['GET'])
def FollowingLatestPhoto(request):
    # 값 받아오기
    email = request.GET.get('email')
    
    # 내가 팔로우 하는 친구email조회(읽지 않은 사진)
    follow_queryset = Follow.objects.filter(Q(email=email),Q(read=False))
    follow_serializer = FollowSerializer(follow_queryset, many=True)
    
    real_result_list = []
    for follow in follow_serializer.data:
        # 친구email
        f_u_email = follow['following_user_id']
        # 친구email을 통해 '이미지'와 '날짜' 가져옴(날짜 내림차순)
        photo_queryset = Photo.objects.filter(email=f_u_email).order_by('-reg_date')[:1]
        photo_serializer = PhotoSerializer(photo_queryset, many=True)
        result_list = []
        for photo in photo_serializer.data:
            result_dict = {}
            email = photo['email']
            url = photo['url']
            reg_date = photo['reg_date']
            result_dict['email'] = email
            result_dict['url'] = url
            result_dict['reg_date'] = reg_date

            # 친구email을 통해 '이름' 가져옴
            name = UserInfo.objects.get(email=email).name
            result_dict['name'] = name
        real_result_list.append(result_dict)
    return Response(real_result_list)




# 사진 읽음 표시
# 받는 값(json) : email, following_user_id
# 만든이 : snchoi
@api_view(['PUT'])
def FollowPhotoRead(request):
    params = request.data
    email = params['email']
    following_user_id = params['following_user_id']

    follow = Follow.objects.get(email=email,following_user_id=following_user_id)
    follow.read = True
    try:
        follow.save()
        print('읽음 완료')
        return Response({"result":True}, status=status.HTTP_201_CREATED)
    except:
        return Response({"result":False}, status=status.HTTP_400_BAD_REQUEST)
