from django.db import models
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from datetime import datetime



# 냉장고
class Refrigerator(models.Model):
    fridge_number = models.CharField(max_length=50, primary_key=True) #PK(냉장고PK)
    email = models.CharField(max_length=50, null=True) # FK(사용자id값)
    manutactor_date = models.DateField
    outing_mode = models.IntegerField(default=0)
    motion_period = models.IntegerField(default=1)
    alarm_mode = models.IntegerField(default=0)

    class Meta:
        db_table = 'REFRIGERATOR'

    def __str__(self):
        return self.fridge_number


# 사진
class Photo(models.Model):
    id = models.AutoField(primary_key=True) #PK(냉장고 사진PK)
    email = models.CharField(max_length=50, null=True) # FK(사용자id값)
    file_name = models.CharField(max_length=50, null=True)
    url = models.CharField(max_length=500, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)


    class Meta:
        db_table = 'PHOTO'

    def __int__(self):
        return self.id

# 센서
class Sensor(models.Model):
    id = models.AutoField(primary_key=True) #PK(냉장고 사진PK)
    email = models.CharField(max_length=50, null=True) # FK(사용자id값)
    name = models.CharField(max_length=50, null=True)
    value = models.IntegerField(blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)


    class Meta:
        db_table = 'SENSOR'

    def __str__(self):
        return self.name

