from django.urls import path, include
from .views import HelloAPI
from . import views

urlpatterns = [
    # Test
    path('api/test/', views.HelloAPI),
]