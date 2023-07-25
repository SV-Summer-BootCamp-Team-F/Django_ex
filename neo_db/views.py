# views.py
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer, CardSerializer, HAVESerializer, RelationSerializer
from rest_framework import views
from py2neo import Graph
from .models import USER, CARD
from rest_framework import status, views
from neo4j import GraphDatabase, basic_auth

#cardupdate 파일
from rest_framework import status, views
from rest_framework.response import Response
from neo4j import GraphDatabase, basic_auth
from .serializers import CardSerializer

from neomodel import config
from django.conf import settings

config.DATABASE_URL = settings.NEO4J_BOLT_URL
config.DATABASE_AUTH = (settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)

# Neo4j 드라이버 생성
driver = GraphDatabase.driver(config.DATABASE_URL, auth=basic_auth(*config.DATABASE_AUTH))

import  uuid
class RegisterView(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # 필수 항목 확인
            if 'user_email' not in data or 'password' not in data:
                return Response({"message": "이메일과 비밀번호는 필수로 입력해야 합니다.", "result": None},
                                status=status.HTTP_400_BAD_REQUEST)



            with driver.session() as session:
                # 전화번호 중복 확인
                result = session.run("MATCH (user:User) WHERE user.phone = $user_phone RETURN user",
                                     {"user_phone": data['user_phone']})
                if result.single():
                    return Response({"message": "이미 존재하는 전화번호입니다.", "result": None}, status=status.HTTP_204_NO_CONTENT)
                # 이메일 중복 확인
                result = session.run("MATCH (user:User) WHERE user.email = $email RETURN user",
                                     {"email": data['user_email']})


                # 새로운 사용자 추가
                # UUID 생성
                uid = str(uuid.uuid4())
                data['uid'] = uid
                # 업데이트는 노드에 보이지 않음
                r = session.run("""
                    CREATE (user:User {
                        uid: $uid,
                        name: $user_name,
                        email: $user_email,
                        password: $password,
                        phone: $user_phone,
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


        with driver.session() as session:
            # Query to find user with provided email and password
            query = f"MATCH (n:User) WHERE n.email = '{user_email}' AND n.password = '{password}' RETURN n"
            result = session.run(query).data()
            print(result)
            if len(result) == 0:
                return Response({'message': '로그인 실패, 유효하지 않은 이메일 혹은 비밀번호입니다.'}, status=status.HTTP_401_UNAUTHORIZED)

            res = {
                "message": "로그인 성공",
                "result": {
                    "user_email": user_email,
                    "uid": result[0]['n']['uid']
                }
            }
            return Response(res, status=status.HTTP_200_OK)





class UserInfoView(views.APIView):
    def get(self, request, user_uid, format=None):

        with driver.session() as session:
            # user_uid를 사용하여 사용자 정보를 검색
            result = session.run("MATCH (user:User) WHERE user.uid = $user_uid RETURN user", user_uid=user_uid)
            record = result.single()
            if record:
                user_info = record['user']
                res = {
                    "message": "유저정보 불러오기 성공",
                    "result": {
                        "user_name": user_info['name'],
                        "user_email": user_info['email'],
                        "password": user_info['password'],
                        "user_phone": user_info['phone'],
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
                        phone: $user_phone,
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
        user_uid = request.data.get('user_uid')  # 'user_uid'를 request에서 추출
        serializer = CardSerializer(data={**request.data, 'user_uid': user_uid})  # 'user_uid'를 serializer에 전달
        if serializer.is_valid():
            data = serializer.validated_data

            with driver.session() as session:
                # 카드 추가
                session.run("""
                    CREATE (card:Card {
                        name: $card_name,
                        email: $card_email,
                        phone: $card_phone,
                        intro: $card_intro,
                        photo: $card_photo,
                        created_at: date($created_at)
                    })
                """, **data)

                # 동일한 uid를 가진 유저를 찾아 카드와 연결 (HAVE 관계로 연결)
                session.run("""
                    MATCH (user:User), (card:Card)
                    WHERE user.uid = $uid AND card.phone = $phone
                    MERGE (user)-[r:HAVE]->(card)
                """, uid=user_uid, phone=data['card_phone'])  # 'uid'를 사용하여 사용자를 찾아 카드와 연결

            return Response({
                "message": "본인 명함 등록 성공",
                "result": data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CardUpdateView(views.APIView):
    def put(self, request, card_id=None, *args, **kwargs):
        card_id = request.data.get('card_id', None)
        if card_id is None:
            return Response({"message": "명함 아이디가 필요합니다.", "result": None}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data


            with driver.session() as session:
                # 명함 정보 확인
                result = session.run("MATCH (card:Card) WHERE id(card) = $card_id RETURN card", card_id=int(card_id))
                if not result.single():
                    return Response({"message": "존재하지 않는 명함입니다.", "result": None}, status=status.HTTP_204_NO_CONTENT)

                # 명함 정보 수정
                session.run("""
                    MATCH (card:Card)
                    WHERE id(card) = $card_id
                    SET card += {
                        name: $card_name,
                        email: $card_email,
                        intro: $card_intro,
                        photo: $card_photo,
                        updated_at: datetime()  // 현재 시간으로 업데이트
                    }
                """, card_id=int(card_id), **data)

            return Response({
                "message": "명함정보 수정 성공",
                "result": data
            }, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#관계 전체 보기

#명함과 유저에 관계 설정
class UserRelationView(APIView):
    def post(self, request, user_id):  # 인자 이름을 user_id로 변경했습니다.
        data = request.data
        user_id2 = data.get('user_id2')
        relation_name = data.get('relation_name')
        memo = data.get('memo')


        with driver.session() as session:
            # Check if both users exist
            result1 = session.run("MATCH (user:User) WHERE id(user) = $user_id RETURN user", {"user_id": user_id})
            user1 = result1.single()
            result2 = session.run("MATCH (user:User) WHERE id(user) = $user_id2 RETURN user", {"user_id2": user_id2})
            user2 = result2.single()
            if not user1 or not user2:
                return Response({"message": "하나 또는 두 사용자가 등록되지 않았습니다.", "result": None},
                                status=status.HTTP_202_ACCEPTED)

            # Create relation
            session.run("""
                   MATCH (user1:User), (user2:User)
                   WHERE id(user1) = $user_id AND id(user2) = $user_id2
                   CREATE (user1)-[relation:RELATION {relation_name: $relation_name, memo: $memo}]->(user2)
                   RETURN type(relation)
               """, {"user_id": user_id, "user_id2": user_id2, "relation_name": relation_name, "memo": memo})
        return Response({"message": "관계 정보 만들기 성공", "result": {"user_id2": user_id2, "relation_name": relation_name}},
                        status=status.HTTP_201_CREATED)