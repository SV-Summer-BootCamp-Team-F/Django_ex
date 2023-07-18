from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Users
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_name', 'user_email', 'phone_num', 'created_at', 'updated_at', 'delete_at']

