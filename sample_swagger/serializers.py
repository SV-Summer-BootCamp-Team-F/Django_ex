from rest_framework import serializers
from .models import User
from .models import Card
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'user_name', 'user_email', 'phone_num', 'user_photo', 'created_at', 'update_at', 'delete_at')
        extra_kwargs = {
            'password': {'write_only': True},
        }
        #추가적인 필드 설정 지정
        # password 필드 적성 전용 설정. 즉, 응답 시 클라이언트에게 보여주지 않음



    def create(self, validated_data):
        #직렬화 된 데이터 기반으로 모델 인스턴스 생성
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'user', 'card_name', 'card_email', 'card_num', 'card_intro', 'card_photo', 'created_at',
                          'updated_at']

class CardSerializer:
    pass