
# views.py
from rest_framework import status, views
from rest_framework.response import Response
from neo4j import GraphDatabase, basic_auth
from .serializers import UserSerializer

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


