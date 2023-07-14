from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.decorators import api_view #api
from rest_framework.response import Response #api




@api_view(['GET'])
def get(request):
    return Response(request)


@api_view(['POST'])
def post(request):
    return Response(request)


