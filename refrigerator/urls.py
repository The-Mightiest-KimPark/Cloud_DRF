from django.urls import path, include
from . import views

urlpatterns = [
    # path('api/fridge-verify/', views.FridgeNumberVerification),
    path('api/insert-email-to-fridge/', views.InsertUserInfoToFridge),
    path('api/going-out-mode/',views.GoingOutMode),
    path('api/sensorvalue/', views.SensorValue),
]