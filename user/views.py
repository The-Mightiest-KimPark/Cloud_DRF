from django.shortcuts import render
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, generics, status, filters

from refrigerator.models import Photo
from refrigerator.serializers import PhotoSerializer
from .serializers import UserInfoSerializer, FollowSerializer, RecipeFavoriteSerializer, UserViewSerializer, AlarmSerializer
from .models import UserInfo, Follow, RecipeFavorite, Alarm
from themightiestkpk.settings import SECRET_KEY
from bigdata.models import AllRecipe
from bigdata.serializers import AllRecipeSerializer
from ai.models import AllGrocery
from ai.serializers import AllGrocerySerializer

import json
import bcrypt
import jwt



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
    follow_queryset = Follow.objects.filter(Q(email=email),Q(read=0))
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
    follow.read = 1
    try:
        follow.save()
        print('읽음 완료')
        return Response({"result":True}, status=status.HTTP_201_CREATED)
    except:
        return Response({"result":False}, status=status.HTTP_400_BAD_REQUEST)


# 회원가입
# 받는 값(json) : email, age, sex, phone_number, name, password, guardian_name, guardian_phone_number, purpose
# 만든이 : snchoi
@api_view(['POST'])
def SignUp(request):
    data = request.data
    try:
        # 존재하는 이메일 이라면
        if UserInfo.objects.filter(email=data['email']).exists():
            return Response({"result":False}, status=status.HTTP_400_BAD_REQUEST)
        
        # 비밀번호 암호화
        password = data['password'].encode('utf-8')
        password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())
        password_crypt = password_crypt.decode('utf-8')

        UserInfo(
            email=data['email'],
            age=data['age'],
            sex=data['sex'],
            phone_number=data['phone_number'],
            name=data['name'],
            password=password_crypt,
            guardian_name=data['guardian_name'],
            guardian_phone_number=data['guardian_phone_number'],
            purpose=data['purpose'],
            img_url=None
        ).save()

        return Response({"result":True}, status=status.HTTP_201_CREATED)

    except KeyError:
        return Response({"message":"INVALID_KEYS"}, status=status.HTTP_400_BAD_REQUEST)

# 로그인
# 받는 값(json) : email, password
# 만든이 : snchoi
@api_view(['POST'])
def SignIn(request):
    data = request.data
    try:
        if UserInfo.objects.filter(email=data['email']).exists():
            user = UserInfo.objects.get(email=data['email'])

            # 비밀번호 확인
            # 사용자가 입력한 비밀번호를 인코딩하고, 사용자의 이메일과 매칭되는 DB의 비밀번호를 찾아와서 인코딩. 이 두 값을 bcrypt.checkpw로 비교하면 됨
            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                # 토큰 발행
                token = jwt.encode({'email':data['email']}, SECRET_KEY, algorithm='HS256')
                token = token.decode('utf-8')

                return Response({"token":token}, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            Response(status=status.HTTP_400_BAD_REQUEST)
    
    except KeyError:
        return Response({"message":"INVALID_KEYS"}, status=status.HTTP_400_BAD_REQUEST)

# 토큰 체크(인가된 사용자인지 확인)
# 받는 값 : token
# 만든이 : snchoi
@api_view(['POST'])
def TockenCheck(request):
    data = request.data
    user_token_info = jwt.decode(data['token'], SECRET_KEY, algorithm = 'HS256')

    if UserInfo.objects.filter(email=user_token_info['email']).exists():
        return Response(status=status.HTTP_200_OK)

    return Response(status=status.HTTP_403_FORBIDDEN)    

# 레시피 즐겨찾기
# 만든이 : snchoi
@api_view(['PUT','GET'])
def RecipeFavorites(request):

    # 레시피 즐겨찾기 등록 / 취소  

    # 받는 값 : email, all_recipe_id       
    if request.method == 'PUT':
        params = request.data
        email = params['email']
        all_recipe_id = params['all_recipe_id']

        # 즐겨찾기 여부 확인
        favorite = RecipeFavorite.objects.filter(Q(email=email),Q(all_recipe_id=all_recipe_id))

        print('favorite : ', favorite)
        
        # 즐겨찾기 했다면
        if favorite: 
            # 즐겨찾기 취소
            try:
                favorite.delete()
                return Response(status=status.HTTP_201_CREATED)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
        
        # 즐겨찾기 하지 않았다면
        else:
            # 즐겨찾기 추가
            serializer = RecipeFavoriteSerializer(data=params)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 즐겨찾기한 레시피 조회
    # 받는 값 : email

    elif request.method == 'GET':
        # 해당 아이디가 즐겨찾기 한 all_recipe_id 조회
        email = request.GET.get('email')

        all_recipe_id_queryset = RecipeFavorite.objects.filter(email=email)
        recipe_serializer = RecipeFavoriteSerializer(all_recipe_id_queryset, many=True)

        # all_recipe_id 값에 해당하는 추천 레시피 값 리턴
        recipe_from_user = []
        for recipe_favorite_info in recipe_serializer.data:
            all_recipe_id = recipe_favorite_info['all_recipe_id']
            all_recipe_queryset = AllRecipe.objects.filter(id=all_recipe_id)
            allrecipe_serializer = AllRecipeSerializer(all_recipe_queryset, many=True)
            recipe_from_user.append(allrecipe_serializer.data[0])
        return Response(recipe_from_user)

# user information
# class MemberDetailView(DetailView):
#     template_name = 'detail.html'
#     model = UserInfo

# 식재료 알림 삽입 / 조회 / 수정 / 삭제
@api_view(['POST','GET','PUT','DELETE'])
def GroceryAlarm(request):

    # 식재료 알림 삽입
    if request.method == 'POST':
        serializer = AlarmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 식재료 수정
    # 받는 값 : email, all_grocery_id, count  
    elif request.method == 'PUT':
        params = request.data
        email = params['email']
        all_grocery_id = params['all_grocery_id']
        count = params['count']

        alarm = Alarm.objects.get(Q(email=email),Q(all_grocery_id=all_grocery_id))
        
        alarm.email = email
        alarm.all_grocery_id = all_grocery_id
        alarm.count = count

        try:
            alarm.save()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # 식재료 알림 삭제
    elif request.method == 'DELETE':
        params = request.data
        email = params['email']
        all_grocery_id = params['all_grocery_id']

        queryset = Alarm.objects.get(Q(email=email),Q(all_grocery_id=all_grocery_id))

        try:
            queryset.delete()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    
    # 알림 체크한 값 조회
    # 받는 값 : email
    elif request.method == 'GET':
        # 사용자 아이디에 해당하는 알림 등록값 조회
        email = request.GET.get('email')
        all_grocery_id_queryset = Alarm.objects.filter(email=email)
        grocery_serializer = AlarmSerializer(all_grocery_id_queryset, many=True)

        # 식재료 이름도 같이 보내주기
        # all_grocery_id 값에 해당하는 식료품 조회
        grocery_from_user = []
        for recipe_favorite_info in grocery_serializer.data:
            all_grocery_id = recipe_favorite_info['all_grocery_id']
            all_grocery = AllGrocery.objects.get(id=all_grocery_id)
            recipe_favorite_info['name'] = all_grocery.name        
            grocery_from_user.append(recipe_favorite_info)
        return Response(grocery_from_user)

# 유저 정보
class UserView(generics.ListCreateAPIView):
    # name = "UserInfo"
    # def get(self, request, *args, **kwargs):
    #     email = request.query_params.get("id")
    #     query = UserInfo.id.get(id=email)
    #     serializer = UserViewSerializer(query, many=False)

    #     return Response(serializer.data)
    queryset = UserInfo.objects.all()
    serializer_class = UserViewSerializer
