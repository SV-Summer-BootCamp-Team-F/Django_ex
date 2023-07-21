
# views.py
from django.http import JsonResponse
from neo4j import GraphDatabase, basic_auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer
from rest_framework import views
from py2neo import Graph
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import views, status
from rest_framework.response import Response

class RegisterView(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # Neo4j에 연결
            driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "12345678"))
            with driver.session() as session:
                # 이메일 중복 확인
                result = session.run("MATCH (user:User) WHERE user.email = $email RETURN user", email=data['user_email'])
                if result.single():
                    return Response({"message": "이미 존재하는 이메일입니다.", "result": None}, status=status.HTTP_204_NO_CONTENT)

                # 새로운 사용자 추가
                session.run("""
                    CREATE (user:User {
                        name: $user_name,
                        email: $user_email,
                        password: $password,
                        phone: $phone_num,
                        photo: $user_photo,
                        is_user: $is_user,
                        created_at: date($created_at)
                    })
                """, **data)

            return Response({
                "message": "회원가입 성공",
                "result": data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(views.APIView):
    def post(self, request):
        user_email = request.data.get("user_email")
        password = request.data.get("password")

        # Connect to Neo4j
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "12345678"))
        with driver.session() as session:
            # Query to find user with provided email and password
            query = f"MATCH (n:User) WHERE n.email = '{user_email}' AND n.password = '{password}' RETURN n"
            result = session.run(query).data()

            if len(result) == 0:
                return Response({'message': '로그인 실패, 유효하지 않은 이메일 혹은 비밀번호입니다.'}, status=status.HTTP_401_UNAUTHORIZED)

            res = {
                "message": "로그인 성공",
                "result": {
                    "user_email": user_email,
                }
            }
            return Response(res, status=status.HTTP_200_OK)
