from django.shortcuts import render
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, generics, status, filters
from .serializers import UserInfoSerializer, FollowSerializer, RecipeFavoriteSerializer
from .models import UserInfo, Follow, RecipeFavorite
import json


# 팔로우 / 언팔로우 (받는 값 : email, 팔로우한 상대email)
# 만든이 : snchoi
#  {
# 	"email": "test", 
# 	"following_user_id": "test2"
# }
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
# 받는 값 : 구분값, email, 팔로우한 상대email
# 만든이 : snchoi
@api_view(['GET'])
def FollowingLatestPhoto(request):
    gubun = request.GET.get('gubun')
    pass




# 사진 읽음 표시 (받는 값 : email, 팔로우한 상대email)
# 만든이 : snchoi
# {
# 	"email": "test", 
# 	"following_user_id": "test2"
# }
@api_view(['PUT'])
def FollowPhotoRead(request):
    params = request.data
    email = params['email']
    following_user_id = params['following_user_id']

    follow = Follow.objects.get(email=email,following_user_id=following_user_id)
    follow.read = True
    follow.save()
    print('읽음 완료')
    return Response(status=status.HTTP_201_CREATED)
