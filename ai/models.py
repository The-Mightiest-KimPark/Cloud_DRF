from django.db import models
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from datetime import datetime


# 식재료 
class Grocery(models.Model):
    id = models.AutoField(primary_key=True) #PK(현재식재료PK)
    fridge_number = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=20, null=True)
    count = models.IntegerField(blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)
    gubun = models.CharField(max_length=5, null=True)

    class Meta:
        db_table = 'GROCERY'

    def __str__(self):
        return self.name

