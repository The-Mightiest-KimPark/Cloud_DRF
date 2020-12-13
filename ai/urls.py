from django.urls import path, include
from . import views

urlpatterns = [
    path('api/ai-img-grocery/', views.AiImgGrocery),
    path('api/all-grocery-name/', views.AllGroceryName.as_view()),
    path('api/user-input-grocery/', views.userInputGrocery),
    path('api/test/', views.test),
]