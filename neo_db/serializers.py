# backend/neo_db/serializers.py
from rest_framework import serializers
import bcrypt
from rest_framework import serializers
from .models import USER , CARD, HAS_RELATION

SECRET_KEY = 'django-insecure-ei+d5(j38wpe9abp-nnc3q^sjc+!5bzs-$i=n!-9jj22gem$#w'  # Change this with your own secret key

class UserSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)
    user_email = serializers.EmailField()
    password = serializers.CharField(max_length=50)
    phone_num = serializers.CharField(max_length=20)
    user_photo = serializers.CharField(max_length=5000, allow_blank=True)
    is_user = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    update_at = serializers.DateTimeField()  # 이 줄 추가

    # 모델을 JSON 형태로 변환
    class Meta:
        model = USER
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


from rest_framework import serializers

class CardSerializer(serializers.Serializer):
    card_name = serializers.CharField(max_length=100)
    card_email = serializers.EmailField()
    card_intro = serializers.CharField(max_length=3000, allow_blank=True)
    card_photo = serializers.CharField(max_length=5000)
    created_at = serializers.DateField()
    update_at = serializers.DateTimeField()  # 이 줄 추가
    class Meta:
        model = CARD
        fields = (
            'card_name', 'card_email', 'card_info', 'card_photo',
            'created_at', 'update_at'
        )

class RelationshipSerializer(serializers.ModelSerializer):
    relation_name = serializers.CharField()
    memo = serializers.CharField()
    created_at = serializers.DateTimeField()
    card_id = serializers.CharField(source='card.id')
    card_name = serializers.CharField(source='card.card_name')
    user_photo = serializers.CharField(source='card.user_photo')

    class Meta:
        model = HAS_RELATION
        fields = (
            'relation_name', 'memo', 'created_at', 'card_id', 'card_name', 'user_photo'
        )



