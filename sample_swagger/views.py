from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer
from .models import Users
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Users.objects.all().order_by('created_at')
    #데이터베이스 가져와 최신 사용자부터 정렬된 순서대로 queryset 저장하는 것을 의미
    serializer_class = UserSerializer





