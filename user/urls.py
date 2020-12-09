from django.urls import path, include
from . import views

urlpatterns = [
    path('api/follow/', views.FollowAndUnfollow),
    path('api/follow-read/', views.FollowPhotoRead),
]