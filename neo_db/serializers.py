#serlializers
from rest_framework import serializers
import bcrypt
from neo4j import GraphDatabase, basic_auth
from .models import USER, CARD, HAVE, RELATION  # models 모듈에서 USER, CARD, HAVE 클래스를 불러옵니다.


class UserSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)
    user_email = serializers.EmailField()
    password = serializers.CharField(max_length=50)
    phone_num = serializers.CharField(max_length=20)
    user_photo = serializers.CharField(max_length=5000, allow_blank=True)
    is_user = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    update_at = serializers.DateTimeField()

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        validated_data['password'] = hashed_password.decode('utf-8')

        user = USER(**validated_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    user_email = serializers.EmailField()
    password = serializers.CharField(max_length=50)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        validated_data['password'] = hashed_password.decode('utf-8')

        ## NEO4J QUERY FOR LOGIN OPERATIONS ##

class CardSerializer(serializers.Serializer):
    card_name = serializers.CharField(max_length=100)
    card_email = serializers.EmailField()
    card_intro = serializers.CharField(max_length=3000, allow_blank=True)
    card_photo = serializers.CharField(max_length=5000)
    created_at = serializers.DateTimeField(required=False)
    update_at = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        card = CARD(**validated_data)
        card.save()

        user = USER.nodes.get_or_none(user_email=validated_data['card_email'])
        if user:
            user.cards.connect(card)

        return card

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


# HAVE Serializer는 별도로 필요하지 않을 것으로 보입니다.


class HAVESerializer(serializers.Serializer):
    uid = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def create(self, validated_data):
        # NEO4J QUERY TO CREATE HAVE RELATIONSHIP #

        def update(self, instance, validated_data):
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
        ## NEO4J QUERY TO UPDATE HAVE RELATIONSHIP ##


class RelationSerializer(serializers.Serializer):
    uid = serializers.UUIDField(read_only=True)
    relation_name = serializers.CharField(required=True)
    memo = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return RELATION.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.relation_name = validated_data.get('relation_name', instance.relation_name)
        instance.memo = validated_data.get('memo', instance.memo)
        instance.save()
        return instance