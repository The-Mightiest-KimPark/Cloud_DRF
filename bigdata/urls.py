from django.urls import path, include
from .views import BdRecommRecipe
from . import views

urlpatterns = [
    path('api/bd-recomm-recipe/', views.BdRecommRecipe),
]