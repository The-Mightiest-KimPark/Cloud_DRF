from django.db import models
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from datetime import datetime


# 식재료 기반 추천 레시피
class RecommRecipe(models.Model):
    id = models.AutoField(primary_key=True) #PK(추천레시피PK)
    refri_number = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=20, null=True)
    ingredient = models.CharField(max_length=50, null=True)
    ingredient_name = models.CharField(max_length=50, null=True)
    seasoning = models.CharField(max_length=50, null=True)
    seasoning_name = models.CharField(max_length=50, null=True)
    howto = models.CharField(max_length=500, null=True)
    purpose = models.CharField(max_length=20, null=True)
    views = models.IntegerField(blank=True, null=True)
    img = models.CharField(max_length=100, null=True)
    recipe_num = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'RECOMM_RECIPE'

    def __str__(self):
        return self.name

