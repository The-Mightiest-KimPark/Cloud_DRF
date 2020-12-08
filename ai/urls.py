from django.urls import path, include
from . import views

urlpatterns = [
    path('api/ai-img-grocery/', views.AiImgGrocery),
]