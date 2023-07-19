# neo_db/serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_name', 'password', 'user_email','phone_num','user_photo','is_user','created_at')
