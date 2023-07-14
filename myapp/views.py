from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

class LoginView(APIView):
    def post(self, request):
        # 로그인 로직 작성
        # ...

        return Response({"message": "로그인 성공"})


class MyAPIView:
    pass