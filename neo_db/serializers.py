from rest_framework import serializers
import bcrypt

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

        ## NEO4J QUERY TO CREATE USER NODE ##

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        ## NEO4J QUERY TO UPDATE USER NODE ##


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


    ## NEO4J QUERY FOR CARD RELATED OPERATIONS ##

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        validated_data['password'] = hashed_password.decode('utf-8')

        ## NEO4J QUERY TO CREATE USER NODE ##

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)


class RelationshipSerializer(serializers.Serializer):
    relation_name = serializers.CharField()
    memo = serializers.CharField()
    created_at = serializers.DateTimeField()
    card_id = serializers.CharField()
    card_name = serializers.CharField()
    user_photo = serializers.CharField()

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

    ## NEO4J QUERY FOR RELATIONSHIP RELATED OPERATIONS ##
