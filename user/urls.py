from django.urls import path, include
from django.conf.urls import url
from django.views.generic import RedirectView
from . import views
from .views import *

urlpatterns = [
    path('api/follow/', views.FollowAndUnfollow),
    path('api/follow-read/', views.FollowPhotoRead),
    path('api/follow-latest-photo/', views.FollowingLatestPhoto),
    path('api/follow-userinfo/', views.FollowUserInfo),

    path('api/sign-up/', views.SignUp),
    path('api/sign-in/', views.SignIn),

    path('api/token-check/', views.TockenCheck),
    path('api/recipe-favorite/', views.RecipeFavorites),
    # path('<str:pk>/detail', views.MemberDetailView.as_view(), 'detail'),
    path('api/user-info/', views.UserView.as_view()),
    path('api/grocery-alarm/', views.GroceryAlarm),
    path('api/user-modify/', views.UserModify),
]