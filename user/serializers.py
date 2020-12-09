from rest_framework import serializers
from .models import UserInfo, Follow, RecipeFavorite
from refrigerator.models import Photo


# 사용자
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields= '__all__'

# 팔로우
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields= '__all__'

# 레시피 즐겨찾기
class RecipeFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeFavorite
        fields= '__all__'

# # 팔로우 최신 사진 조회
# class CustomizingFollowSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(read_only=True)
#     class Meta:
#         model = Photo
#         fields= ('email, url, reg_date, name')
