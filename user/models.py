from django.db import models
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



# 사용자
class UserInfo(models.Model):
    email = models.CharField(primary_key=True,max_length=50) # PK(사용자PK)
    age = models.IntegerField(blank=True,null=True)
    sex = models.IntegerField(blank=True,null=True)
    phone_number = models.CharField(max_length=500, null=True)
    name = models.CharField(max_length=500, null=True)
    password = models.CharField(max_length=500, null=True)
    guardian_name = models.CharField(max_length=500, null=True)
    guardian_phone_number = models.CharField(max_length=500, null=True)
    purpose = models.CharField(max_length=500, null=True)
    img_url = models.CharField(max_length=500, null=True)

    class Meta:
        db_table = 'USER_INFO'

    def __int__(self):
        return self.id



# 팔로우
class Follow(models.Model):
    id = models.AutoField(primary_key=True) #PK(냉장고 사진PK)
    email = models.CharField(max_length=50, null=True) # FK(사용자id값)
    following_user_id = models.CharField(max_length=500, null=True)
    read = models.BooleanField(default=False)

    class Meta:
        db_table = 'FOLLOW'

    def __int__(self):
        return self.id

# 레시피 즐겨찾기
class RecipeFavorite(models.Model):
    id = models.AutoField(primary_key=True) #PK(레시피 즐겨찾기PK)
    email = models.CharField(max_length=50, null=True) # FK(사용자id값)
    all_recipe_id = models.IntegerField(blank=True, null=True) 

    class Meta:
        db_table = 'RECIPE_FAVORITE'

    def __int__(self):
        return self.id

# 식재료 알림
class Alarm(models.Model):
    id = models.AutoField(primary_key=True) #PK(레시피 즐겨찾기PK)
    email = models.CharField(max_length=50, null=True) # FK(사용자id값)
    all_grocery_id = models.IntegerField(blank=True, null=True)  #FK(식료품id값)
    count = models.IntegerField(blank=True, null=True)


    class Meta:
        db_table = 'ALARM'

    def __int__(self):
        return self.id

