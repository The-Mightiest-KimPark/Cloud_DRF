from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserInfo
# Register your models here.

# class ProfileInline(admin.StackedInline):
#     model = UserInfo
#     can_delete = False
#     verbose_name_plural = 'UserInfo'
#     fk_name = 'email'

# class CustomUserAdmin(UserAdmin):
#     inlines = (ProfileInline, )

#     def get_inline_instances(self, request, obj=None):
#         if not obj:
#             return list()
#         return super(CustomUserAdmin, self).get_inline_instances(request, obj)

# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)

