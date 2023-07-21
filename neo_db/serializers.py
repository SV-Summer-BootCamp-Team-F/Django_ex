# backend/neo_db/serializers.py
from rest_framework import serializers
import bcrypt
from rest_framework import serializers
from .models import User

SECRET_KEY = 'django-insecure-ei+d5(j38wpe9abp-nnc3q^sjc+!5bzs-$i=n!-9jj22gem$#w'  # Change this with your own secret key

class UserSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)
    user_email = serializers.EmailField()
    password = serializers.CharField(max_length=50)
    phone_num = serializers.CharField(max_length=20)
    user_photo = serializers.CharField(max_length=5000, allow_blank=True)
    is_user = serializers.BooleanField()
    created_at = serializers.DateTimeField()

    class Meta:
        model = User
        fields = (
            'user_name', 'user_email', 'password', 'phone_num', 'user_photo',
            'is_user', 'created_at', 'update_at', 'delete_at')


class LoginSerializer(serializers.Serializer):
    user_email = serializers.EmailField()
    password = serializers.CharField(max_length=50)
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        validated_data['password'] = hashed_password.decode('utf-8')
        return validated_data
