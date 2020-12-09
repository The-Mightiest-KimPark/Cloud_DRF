from django.db import models
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from datetime import datetime


# 사진
class PhotoTest(models.Model):
    id = models.AutoField(primary_key=True) #PK(냉장고 사진PK)
    fridge_number = models.CharField(max_length=50, null=True)
    url = models.CharField(max_length=500, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)


    class Meta:
        db_table = 'PHOTO_TEST'

    def __int__(self):
        return self.id

