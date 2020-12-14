from django.urls import path, include
from . import views

urlpatterns = [
    path('api/follow/', views.FollowAndUnfollow),
    path('api/follow-read/', views.FollowPhotoRead),
    path('api/follow-latest-photo', views.FollowingLatestPhoto),
    path('api/sign-up/', views.SignUp),
    path('api/sign-in/', views.SignIn),
    path('api/recipe-favorite/', views.RecipeFavorites)
]