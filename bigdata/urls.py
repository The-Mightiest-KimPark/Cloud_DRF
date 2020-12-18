from django.urls import path, include
from .views import BdRecommRecipe
from . import views

urlpatterns = [
    path('api/bd-recomm-recipe/', views.BdRecommRecipe),
    path('api/recomm-recipe/', views.RecommRecipeGet),
    path('api/recomm-recipe-one/', views.RecommRecipeGetOne),
    path('api/recomm-recipe-detail/', views.RecommRecipeDetail),
]