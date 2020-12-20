from django.urls import path, include
from .views import BdRecommRecipe
from . import views

urlpatterns = [
    path('api/bd-recomm-recipe/', views.BdRecommRecipe),
    path('api/recomm-recipe/', views.RecommRecipeGet),
    path('api/recomm-recipe-purpose/', views.RecommRecipePurposeGet),
    path('api/recomm-recipe-one/', views.RecommRecipeGetOne),
    path('api/recomm-recipe-detail/', views.RecommRecipeDetail),
    path('api/answer-count/', views.AnswerCountGet),
    path('api/answer-save/', views.SaveCountGet)
]