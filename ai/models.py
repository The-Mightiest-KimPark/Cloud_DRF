from django.db import models
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from datetime import datetime


# # 자격증 카테고리 예) 정보통신
# class Category(models.Model):
#     cat_id = models.IntegerField(primary_key=True) #PK(카테고리PK)
#     name = models.CharField(max_length=50) #카테고리 이름
    
#     class Meta:
#         db_table = 'CATEGORY'

#     def __str__(self):
#         return self.name

# # 자격증 예) 정보처리기사
# class Certificate(models.Model):
#     cert_id = models.IntegerField(primary_key=True) #PK(자격증PK)
#     cat_id = models.ForeignKey(Category, related_name="certificates", on_delete=models.CASCADE) #FK(카테고리PK)
#     name = models.CharField(max_length=100) #자격증 이름
#     department = models.CharField(max_length=100) #시행기관
#     pass_percent = models.FloatField(max_length=50, blank=True, null=True) #합격률
#     pass_percent_sil = models.FloatField(max_length=50, blank=True, null=True) #합격률
#     cost = models.CharField(max_length=500, blank=True, null=True) #응시료
#     cost_sil = models.CharField(max_length=500, blank=True, null=True) #응시료
#     examinee = models.IntegerField(default=0, blank=True, null=True) #응시자 수
#     examinee_sil = models.IntegerField(default=0, blank=True, null=True) #응시자 수
#     link = models.CharField(max_length=500, blank=True, null=True)

#     class Meta:
#         db_table = "CERTIFICATE"

#     def __str__(self):
#         return self.name

