#serlializers
#(여기는 필수항목리아고 뜨는 json문에 대한 응답을 보여주는 항목들이라고 생각하시면 됩니다~ 아 노드의 들어가는 것들을 나열한 거라고 생각하세요~)
from rest_framework import serializers
import bcrypt
from neo4j import GraphDatabase, basic_auth
from .models import USER, CARD, HAVE, RELATION  # models 모듈에서 USER, CARD, HAVE 클래스를 불러옵니다.


class UserSerializer(serializers.Serializer):
    user_uid = serializers.UUIDField(required=False)
    user_name = serializers.CharField(max_length=100)
    user_email = serializers.EmailField()
    password = serializers.CharField(max_length=50)
    user_phone = serializers.CharField(max_length=20)
    user_photo = serializers.CharField(max_length=5000, allow_blank=True, required=False)
    is_user = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    #updated_at = serializers.DateTimeField()


    def create(self, validated_data):
        password = validated_data.pop('password', None)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        validated_data['password'] = hashed_password.decode('utf-8')

        # user_photo 필드를 체크하여 값이 없는 경우 기본 이미지 URL로 설정
        user_photo = validated_data.get('user_photo')
        if not user_photo.strip():  # 공백 문자만으로 이루어진 경우도 처리
            validated_data[
                'user_photo'] = 'https://blog.kakaocdn.net/dn/EZGfg/btrEJIAOElH/8IlocIaObhbFMG4HPZAmH1/img.png'
        # 기본 이미지 URL로 설정

        user = USER(**validated_data)
        user.save()
        return user  # 생성된 유저 인스턴스를 반환합니다.

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

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class CardSerializer(serializers.Serializer):
    card_uid = serializers.UUIDField(required=False) #추가
    card_name = serializers.CharField(max_length=100)
    card_email = serializers.EmailField()
    card_phone = serializers.CharField(max_length=20)
    card_intro = serializers.CharField(max_length=3000, allow_blank=True)
    card_photo = serializers.CharField(max_length=5000)
    created_at = serializers.DateTimeField(required=False)
    update_at = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        card = CARD(**validated_data)
        card.save()

        user_uid = validated_data.get('user_uid')  # 유저의 uid를 가져옵니다.
        if user_uid:
            user = USER.nodes.get_or_none(uid=user_uid)  # uid를 사용하여 유저를 찾습니다.
            if user:
                user.cards.connect(card)  # 유저와 카드 사이에 HAVE 관계를 생성합니다.

        return card

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class HAVESerializer(serializers.Serializer):
    have_uid = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def create(self, validated_data):
        def update(self, instance, validated_data):
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

class RelationSerializer(serializers.Serializer):
    relation_uid = serializers.UUIDField(read_only=True)
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