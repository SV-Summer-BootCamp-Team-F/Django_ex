from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from .models import User
from .serializers import UserSerializer
from neo4j import GraphDatabase

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        try:
            # Django ORM으로 유효성 검사 실행
            serializer.instance.full_clean()
            instance = serializer.save()
        except ValidationError as e:
            if '이미 존재하는 이메일입니다.' in e.messages:
                raise Exception("이메일 중복")
            elif '이미 존재하는 전화번호입니다.' in e.messages:
                raise Exception("전화번호 중복")
            else:
                raise

        # Neo4j에 노드 생성
        driver = GraphDatabase.driver("bolt://localhost:7689", auth=("neo4j", "12345678"))
        with driver.session() as session:
            session.run(
                "CREATE (:Person {name: $name, password: $password, email: $email, phone_num: $phone_num, "
                "user_photo: $user_photo, created_at: $created_at})",
                name=instance.user_name, password=instance.password, email=instance.user_email,
                phone_num=instance.phone_num, user_photo=instance.user_photo, created_at=instance.created_at
            )


        # Neo4j에 노드 생성
        #driver = GraphDatabase.driver("bolt://localhost:7689", auth=("neo4j", "12345678"))
        #with driver.session() as session:
        #    session.run(
        #        "CREATE (:Person {name: $name, password: $password, email: $email, phone_num: $phone_num, "
        #        "user_photo: $user_photo, created_at: $created_at})",
        #        name=instance.user_name, password=instance.password, email=instance.user_email,
        #        phone_num=instance.phone_num, user_photo=instance.user_photo, created_at=instance.created_at
          #  )         )