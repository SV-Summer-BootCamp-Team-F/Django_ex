# views.py
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer, CardSerializer, HAVESerializer, RelationSerializer, \
    UserRegisterSerializer
from rest_framework import views
from py2neo import Graph
from .models import USER, CARD
from rest_framework import status, views
from neo4j import GraphDatabase, basic_auth
from neomodel import db

# cardupdate 파일
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

import uuid


# 유저 정보 등록
class RegisterView(views.APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
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
                if result.single():
                    return Response({"message": "이미 존재하는 이메일입니다.", "result": None}, status=status.HTTP_204_NO_CONTENT)

                # 새로운 사용자 추가
                # 업데이트는 노드에 보이지 않음
                r = session.run("""
                    CREATE (user:User {
                        uid: $user_uid,
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


# 유저와 유저 연결
class UserRelationView(APIView):
    def post(self, request):
        data = request.data
        user_uid = data.get('user_uid')  # Get user_uid from request data
        user_phone = data.get('user_phone')
        relation_name = data.get('relation_name')
        memo = data.get('memo')

        with driver.session() as session:
            result = session.run("MATCH (u:User {uid: $user_uid}) RETURN u.uid as user_uid", user_uid=user_uid)
            user1 = result.single()
            if user1 is None:
                logging.error("User with uid %s not found", user_uid)
                return Response({"message": "uid를 찾을 수 없습니다.", "result": None},
                                status=status.HTTP_400_BAD_REQUEST)

            result = session.run("MATCH (u:User {phone: $user_phone}) RETURN u", user_phone=user_phone)
            user2 = result.single()
            if user2 is None:
                logging.error("User with phone %s not found", user_phone)
                return Response({"message": "전화번호를 찾을 수 없습니다.", "result": None},
                                status=status.HTTP_400_BAD_REQUEST)

            # Connect the users with the relation
            session.run("""
                MATCH (u1:User), (u2:User)
                WHERE u1.uid = $uid1 AND u2.phone = $phone2
                MERGE (u1)-[r:RELATION {relation_name: $name, memo: $memo}]->(u2)
            """, uid1=user1['user_uid'], phone2=user_phone, name=relation_name, memo=memo)

        return Response({"message": "회원 끼리 연결 성공",
                         "result": {"user_uid": user_uid,
                                    "user_phone": user_phone,
                                    "relation_name": relation_name,
                                    "memo": memo}},
                        status=status.HTTP_201_CREATED)


# 로그인
class LoginView(views.APIView):
    def post(self, request):
        user_email = request.data.get("user_email")
        password = request.data.get("password")

        with driver.session() as session:
            query = f"MATCH (n:User) WHERE n.email = '{user_email}' AND n.password = '{password}' RETURN n"
            result = session.run(query).data()
            print(result)
            if len(result) == 0:
                return Response({'message': '로그인 실패, 유효하지 않은 이메일 혹은 비밀번호입니다.'},
                                status=status.HTTP_401_UNAUTHORIZED)

            res = {
                "message": "로그인 성공",
                "result": {
                    "user_uid": result[0]['n']['uid']
                }
            }
            return Response(res, status=status.HTTP_200_OK)


# 유저 정보 불러오기
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

            return Response(data=res, status=status.HTTP_200_OK)


# 유저 정보 업데이트
class UserUpdateView(views.APIView):
    def put(self, request, *args, **kwargs):
        user_uid = request.data.get('user_uid', None)
        if user_uid is None:
            return Response({"message": "유저 UID가 필요합니다.", "result": None}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            with driver.session() as session:
                # 이메일 중복 확인 제외
                result = session.run("MATCH (user:User) WHERE user.uid = $user_uid RETURN user", {"user_uid": user_uid})
                if not result.single():
                    return Response({"message": "존재하지 않는 유저입니다.", "result": None}, status=status.HTTP_204_NO_CONTENT)

                # 사용자 정보 수정
                session.run("""
                       MATCH (user:User)
                       WHERE user.uid = $user_uid
                       SET user += {
                           name: $user_name,
                           email: $user_email,
                           password: $password,
                           phone: $user_phone,
                           photo: $user_photo,
                           is_user: $is_user,
                           created_at: datetime()  // 현재 시간으로 업데이트
                       }
                   """, {"user_uid": user_uid, **data})

            return Response({
                "message": "유저정보 수정 성공",
                "result": data
            }, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 유저 정보 사진 업데이트하기
class UpdateUserPhotoView(views.APIView):
    def put(self, request, user_uid):  # url에서 user_uid를 파라미터로 받습니다
        user_photo = request.data.get('user_photo')  # 요청에서 user_photo를 얻습니다
        # if user_photo is None:
        #   return Response({"message": "사진 데이터가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        with driver.session() as session:
            # 해당 uid의 사용자 찾기
            result = session.run("MATCH (user:User) WHERE user.uid = $user_uid RETURN user", user_uid=user_uid)
            if not result.single():  # 사용자가 없는 경우
                return Response({"message": "유저 등록이 안돼있음.", "result": None},
                                status=status.HTTP_202_ACCEPTED)
            # 사용자 프로필 사진 업데이트
            session.run("""
                    MATCH (user:User)
                    WHERE user.uid = $user_uid
                    SET user.photo = $user_photo
               """, user_uid=user_uid, user_photo=user_photo)

        return Response({
            "message": "유저프로필사진 수정 성공",
        }, status=status.HTTP_202_ACCEPTED)


# 명함 등록 및 연결선 생성
class CardAddView(views.APIView):
    def post(self, request):
        user_uid = request.data.get('user_uid')  # 'user_uid'를 request에서 추출
        serializer = CardSerializer(data={**request.data, 'user_uid': user_uid})  # 'user_uid'를 serializer에 전달
        if serializer.is_valid():
            data = serializer.validated_data
            # 전화번호 기준
            with driver.session() as session:
                uid = str(uuid.uuid4())
                data['card_uid'] = uid
                # 카드 추가
                session.run("""
                    CREATE (card:Card {
                        uid: $card_uid,
                        name: $card_name,
                        email: $card_email,
                        phone: $card_phone,
                        intro: $card_intro,
                        photo: $card_photo,
                        created_at: date($created_at)
                    })
                """, **data)

                # 전화번호가 같은 유저를 찾아 카드와 연결 (HAVE 관계로 연결)
                session.run("""
                    MATCH (user:User), (card:Card)
                    WHERE user.phone = card.phone AND card.phone = $card_phone
                    MERGE (user)-[r:HAVE]->(card)
                """, card_phone=data['card_phone'])

            return Response({
                "message": "본인 명함 등록 성공",
                "result": data
            }, status=status.HTTP_201_CREATED)

            #uid 연동
            # with driver.session() as session:
            #     uid = str(uuid.uuid4())
            #     data['card_uid'] = uid
            #     # 카드 추가
            #     session.run("""
            #         CREATE (card:Card {
            #             uid: $card_uid,
            #             name: $card_name,
            #             email: $card_email,
            #             phone: $card_phone,
            #             intro: $card_intro,
            #             photo: $card_photo,
            #             created_at: date($created_at)
            #         })
            #     """, **data)
            #
            #     # 동일한 uid를 가진 유저를 찾아 카드와 연결 (HAVE 관계로 연결)
            #     session.run("""
            #         MATCH (user:User {uid: $user_uid}), (card:Card {uid: $card_uid})
            #         MERGE (user)-[r:HAVE]->(card)
            #     """, user_uid=user_uid, card_uid=data['card_uid'])
            #
            # return Response({
            #     "message": "본인 명함 등록 성공",
            #     "result": data
            # }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 카드 정보 불러오기
class CardInfoView(views.APIView):
    def get(self, request, card_uid, format=None):

        with driver.session() as session:
            # card_uid를 사용하여 카드 정보를 검색
            result = session.run("MATCH (card:Card) WHERE card.uid = $card_uid RETURN card", card_uid=card_uid)
            record = result.single()
            if record:
                card_info = record['card']
                res = {
                    "message": "명함정보 불러오기 성공",
                    "result": {
                        "card_name": card_info['name'],
                        "card_email": card_info['email'],
                        "card_phone": card_info['phone'],
                        "card_intro": card_info['intro'],
                        "card_photo": card_info['photo']
                    }
                }
            else:
                res = {
                    "message": "해당 카드가 없습니다.",
                    "result": None
                }
            return Response(res, status=status.HTTP_200_OK)

#
# 캬드 정보 업데이트
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


import logging


# 관계 전체 보기
# 전체 관계 보기(1촌)
class RelationView(views.APIView):
    def get(self, request, user_uid, format=None):
        with driver.session() as session:
            # user_uid를 사용하여 사용자와 그 사용자와 관계를 가진 모든 사용자 정보를 검색
            result = session.run("""
                MATCH (u:User {uid: $user_uid})-[r:RELATION]->(n:User)
                RETURN u.uid as user_uid, n.uid as card_uid, n.name as card_name, n.photo as user_photo, r.relation_name as relation_name
            """, user_uid=user_uid)

            if result.peek() is None:
                return Response({
                    "message": "유저 등록이 안돼있음",
                    "result": None
                }, status=status.HTTP_400_BAD_REQUEST)

            relations = []
            for record in result:
                relation = {
                    "card_uid": record['card_uid'],
                    "card_name": record['card_name'],
                    "user_photo": record['user_photo'],
                    "relation_name": record['relation_name']
                }
                relations.append(relation)

            return Response({
                "message": "관계 전체 로드 성공",
                "result": relations
            }, status=status.HTTP_200_OK)
        if result.peek() is None:
            return Response({
                "message": "유저 등록이 안돼있음",
                "result": None
            }, status=status.HTTP_400_BAD_REQUEST)


# 전체 관계 보기(2촌)
class RelationDeepView(APIView):
    def get(self, request, user_uid, format=None):
        with driver.session() as session:
            # user_uid를 사용하여 사용자와 그 사용자와 관계를 가진 모든 사용자 정보를 검색
            result = session.run("""
                MATCH (u:User {uid: $user_uid})-[:RELATION]->(:User)-[:RELATION]->(n:User)
                WHERE NOT (u)-[:RELATION]->(n)
                RETURN n.uid as card_uid, n.name as card_name, n.photo as user_photo
            """, user_uid=user_uid)

            if result.peek() is None:
                return Response({
                    "message": "유저 등록이 안돼있음",
                    "result": None
                }, status=status.HTTP_400_BAD_REQUEST)

            relations = []
            for record in result:
                relation = {
                    "card_uid": record['card_uid'],
                    "card_name": record['card_name'],
                    "user_photo": record['user_photo'],
                }
                relations.append(relation)

            return Response({
                "message": "관계 전체 로드 성공",
                "result": relations
            }, status=status.HTTP_200_OK)


# 관계 상세 보기
class CardDetailView(views.APIView):
    def get(self, request, card_uid):
        with driver.session() as session:
            result = session.run("""
                MATCH (c:Card) WHERE c.uid = $card_uid 
                RETURN c.uid as uid, c.name as name, c.email as email, c.intro as intro, c.photo as photo, c.phone as phone, c.memo as memo
            """, card_uid=card_uid)
            card = result.single()
            if card is None:
                return Response({"message": "카드를 찾을 수 없습니다.", "result": None},
                                status=status.HTTP_400_BAD_REQUEST)

            card_info = {
                "card_uid": card['uid'],
                "card_name": card['name'],
                "card_email": card['email'],
                "card_intro": card['intro'],
                "card_photo": card['photo'],
                "user_phone": card['phone'],
                "memo": card['memo'],
            }
            return Response({
                "message": "명함 상세정보 로드 성공",
                "result": card_info
            }, status=status.HTTP_200_OK)


# 번호 조회하가
class PhoneInfoView(views.APIView):
    def get(self, request, user_phone):
        with driver.session() as session:
            result = session.run("""
                MATCH (u:User) WHERE u.phone = $user_phone 
                RETURN u
            """, user_phone=user_phone)
            user = result.single()
            if user is None:
                return Response({
                    "message": "번호 조회 실패",
                }, status=status.HTTP_404_NOT_FOUND)

            return Response({
                "message": "번호 조회 성공",
            }, status=status.HTTP_200_OK)
