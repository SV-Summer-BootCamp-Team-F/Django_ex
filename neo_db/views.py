# views.py
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer, CardSerializer, HAVESerializer, RelationSerializer
from rest_framework import views
from py2neo import Graph
from rest_framework_simplejwt.tokens import RefreshToken
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


# Neo4j에 연결
# !!!!!!!!- driver = GraphDatabase.driver("bolt://localhost:7689",auth=basic_auth("neo4j", "12345678")) #1. 하드코딩이라 비추 (수정을 할때 마다 다 수정해줘야하므로 그런거는 세팅에서 값을 가져와 설정을 해둬야 다 변경이 가능합니다! ) 2.매 클래스마다 코딩이 반복됨(맨 상단에 드라이버를 고정해줄거예요,전역변수로 설정할거예요! ) , 이런건 환경변수를  드라이버를 매번 연결해야하면 다 변경해야해서 안좋음
# command+g

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
                result = session.run("MATCH (user:User) WHERE user.phone = $phone_num RETURN user",
                                     {"phone_num": data['phone_num']})
                if result.single():
                    return Response({"message": "이미 존재하는 전화번호입니다.", "result": None}, status=status.HTTP_204_NO_CONTENT)

                # 이메일 중복 확인
                result = session.run("MATCH (user:User) WHERE user.email = $email RETURN user",
                                     {"email": data['user_email']})
                if result.single():
                    return Response({"message": "이미 존재하는 이메일입니다.", "result": None},
                                    status=status.HTTP_204_NO_CONTENT)

                # 새로운 사용자 추가
                # 업데이트는 노드에 보이지 않음
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
       # driver = GraphDatabase.driver("bolt://localhost:7689",auth=basic_auth("neo4j", "12345678"))
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
            with driver.session() as session:
                    # 카드 생성
                session.run("""
                        CREATE (card:Card {
                            name: $card_name,
                            email: $card_email,
                            phone: $card_phone_num,
                            intro: $card_intro,
                            photo: $card_photo,
                            created_at: date($created_at)
                            })
                    """, **data)

                    # 사용자와 카드를 연결
                session.run("""
                        MATCH (user:User), (card:Card)
                        WHERE user.phone_num = $user_phone_num AND card.phone_num = $card_phone_num
                        MERGE (user)-[r:HAVE]->(card)
                    """, {"user_phone_num": user_phone_num, "card_phone_num": card_phone_num})

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

            # Neo4j에 연결
            driver = GraphDatabase.driver("bolt://localhost:7689",auth=basic_auth("neo4j", "12345678"))
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


#관계 수정
# class UpdateRelationView(APIView):
#     def post(self, request, user_id):  # user_id를 인자로 받습니다.
#         data = request.data
#         card_id = data.get('card_id')
#         relation_name = data.get('relation_name')
#         memo = data.get('memo')
#
#         driver = GraphDatabase.driver("bolt://localhost:7689", auth=basic_auth("neo4j", "12345678"))
#         with driver.session() as session:
#             # Check if user exists
#             result = session.run("MATCH (user:User) WHERE id(user) = $user_id RETURN user", {"user_id": user_id})
#             user = result.single()
#             if not user:
#                 return Response({"message": "유저 등록이 안돼있음.", "result": None}, status=status.HTTP_202_ACCEPTED)
#
#             # Check if card exists
#             result = session.run("MATCH (card:Card) WHERE id(card) = $card_id RETURN card", {"card_id": card_id})
#             card = result.single()
#             if not card:
#                 return Response({"message": "카드 정보가 없습니다.", "result": None}, status=status.HTTP_404_NOT_FOUND)
#
#             # Check if relation exists, if so update it, else create it
#             result = session.run("""
#                 MATCH (user:User)-[relation:HAVE]->(card:Card)
#                 WHERE id(user) = $user_id AND id(card) = $card_id
#                 RETURN relation
#             """, {"user_id": user_id, "card_id": card_id})
#             relation = result.single()
#
#             if relation:
#                 # Update relation if it exists
#                 session.run("""
#                     MATCH (user:User)-[relation:HAVE]->(card:Card)
#                     WHERE id(user) = $user_id AND id(card) = $card_id
#                     SET relation.relation_name = $relation_name, relation.memo = $memo
#                     RETURN type(relation)
#                 """, {"user_id": user_id, "card_id": card_id, "relation_name": relation_name, "memo": memo})
#                 message = "관계 정보 업데이트 성공"
#
#             return Response({"message": message, "result": {"card_id": card_id, "relation_name": relation_name}}, status=status.HTTP_201_CREATED)
#
