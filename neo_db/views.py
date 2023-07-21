
# views.py
from django.http import JsonResponse
from neo4j import GraphDatabase, basic_auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer, CardSerializer
from rest_framework import views
from py2neo import Graph
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import views, status
from rest_framework.response import Response
from neo4j import GraphDatabase, basic_auth

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


class UserInfoView(views.APIView):
    def get(self, request, user_id, format=None):
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "12345678"))
        with driver.session() as session:
            # user_id를 사용하여 사용자 정보를 검색
            result = session.run("MATCH (user:User) WHERE id(user) = $user_id RETURN user", user_id=int(user_id))
            record = result.single()
            if record:
                user_info = record['user']
                res = {
                    "message": "유저정보 불러오기 성공",
                    "result": {
                        "user_name": user_info['name'],
                        "user_email": user_info['email'],
                        "password": user_info['password'],
                        "phone_num": user_info['phone'],
                        "user_photo": user_info['photo']
                    }
                }
            else:
                res = {
                    "message": "유저 등록이 안돼있음",
                    "result": None
                }
            return Response(res, status=status.HTTP_200_OK)


class UserUpdateView(views.APIView):
    def put(self, request, *args, **kwargs):
        user_id = request.data.get('user_id', None)
        if user_id is None:
            return Response({"message": "유저 아이디가 필요합니다.", "result": None}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # Neo4j에 연결
            driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "12345678"))
            with driver.session() as session:
                # 이메일 중복 확인 제외
                result = session.run("MATCH (user:User) WHERE id(user) = $user_id RETURN user", user_id=int(user_id))
                if not result.single():
                    return Response({"message": "존재하지 않는 유저입니다.", "result": None}, status=status.HTTP_204_NO_CONTENT)

                # 사용자 정보 수정
                session.run("""
                    MATCH (user:User)
                    WHERE id(user) = $user_id
                    SET user += {
                        name: $user_name,
                        email: $user_email,
                        password: $password,
                        phone: $phone_num,
                        photo: $user_photo,
                        is_user: $is_user,
                        updated_at: datetime()  // 현재 시간으로 업데이트
                    }
                """, user_id=int(user_id), **data)

            return Response({
                "message": "유저정보 수정 성공",
                "result": data
            }, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateUserPhotoView(views.APIView):
        def put(self, request, user_id):  # url에서 user_id를 파라미터로 받습니다
            user_photo = request.data.get('user_photo')  # 요청에서 user_photo를 얻습니다
            if user_photo is None:
                return Response({"message": "사진 데이터가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

            # Neo4j에 연결
            driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "12345678"))
            with driver.session() as session:
                # 해당 id의 사용자 찾기
                result = session.run("MATCH (user:User) WHERE id(user) = $user_id RETURN user", user_id=user_id)
                if not result.single():  # 사용자가 없는 경우
                    return Response({"message": "유저 등록이 안돼있음.", "result": None}, status=status.HTTP_202_ACCEPTED)

                # 사용자 프로필 사진 업데이트
                session.run("""
                    MATCH (user:User)
                    WHERE id(user) = $user_id
                    SET user.photo = $user_photo
                """, user_id=user_id, user_photo=user_photo)

            return Response({
                "message": "유저프로필사진 수정 성공",
            }, status=status.HTTP_202_ACCEPTED)



class CardAddView(views.APIView):
    def post(self, request):
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # Neo4j에 연결
            driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "12345678"))
            with driver.session() as session:
                # 카드 추가
                session.run("""
                    CREATE (card:Card {
                        name: $card_name,
                        email: $card_email,
                        intro: $card_intro,
                        photo: $card_photo,
                        created_at: date($created_at)
                    })
                """, **data)

            return Response({
                "message": "본인 명함 등록 성공",
                "result": data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CardUpdateView(views.APIView):
    def put(self, request, *args, **kwargs):
        user_id = request.data.get('user_id', None)
        if user_id is None:
            return Response({"message": "유저 아이디가 필요합니다.", "result": None}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # Neo4j에 연결
            driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "12345678"))
            with driver.session() as session:
                # 이메일 중복 확인 제외
                result = session.run("MATCH (card:Card) WHERE id(card) = $card_id RETURN card", user_id=int(card_id))
                if not result.single():
                    return Response({"message": "존재하지 않는 유저입니다.", "result": None}, status=status.HTTP_204_NO_CONTENT)

                # 명함 정보 수정
                session.run("""
                    MATCH (card:Card)
                    WHERE id(card) = $card_id
                    SET user += {
                        name: $card_name,
                        email: $card_email,
                        password: $password,
                        intro: $card_intro
                       
                        photo: $user_photo,
                        is_user: $is_user,
                        updated_at: datetime()  // 현재 시간으로 업데이트
                    }
                """, card_id=int(user_id), **data)

            return Response({
                "message": "명함정보 수정 성공",
                "result": data
            }, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
