# serializers.py
from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)
    user_email = serializers.EmailField()
    password = serializers.CharField(max_length=50)
    phone_num = serializers.CharField(max_length=20)
    user_photo = serializers.CharField(max_length=5000, allow_blank=True)
    is_user = serializers.BooleanField()
    created_at = serializers.DateField()