from rest_framework import serializers
from .models import User
from .models import Card
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user_name', 'user_email', 'phone_num', 'created_at', 'updated_at', 'delete_at']


