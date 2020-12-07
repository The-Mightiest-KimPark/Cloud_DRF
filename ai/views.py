from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, generics, status, filters

# Create your views here.
@api_view(['GET'])
def HelloAPI(request):
    return Response("hello world!")