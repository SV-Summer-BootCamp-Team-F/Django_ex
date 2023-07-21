# neo_db/models.py
from neomodel import StructuredNode, StringProperty, BooleanProperty, DateProperty, UniqueIdProperty

class USER(StructuredNode):
    uid = UniqueIdProperty()
    user_name = StringProperty(unique_index=True, required=True)
    user_email = StringProperty(unique_index=True, required=True)
    password = StringProperty(required=True)
    phone_num = StringProperty(required=True)
    user_photo = StringProperty()
    is_user = BooleanProperty(default=True)
    created_at = DateProperty(auto_now_add=True)


#  user_name = StringProperty(max_length=100, )
#     user_email = StringProperty(max_length=50, )
#     password = StringProperty(max_length=50,default='')
#     phone_num = StringProperty(unique_index=True, max_length=20)
#     user_photo = StringProperty(max_length=5000)
#     is_user = BooleanProperty(default=True)
#     delete_at = DateTimeProperty()
#     created_at = DateTimeProperty(default_now=True)
#     updated_at = DateTimeProperty(default=lambda: datetime.now())
#
#     # 사용자(User)와 카드(Card) 간의 관계 정의
#     cards = RelationshipTo('CARD', 'HAVE')

class CARD(StructuredNode):
    card_name = StringProperty(max_length=100)
    card_email = StringProperty(unique_index=True, max_length=50,)
    card_intro = StringProperty(max_length=3000)
    card_photo = StringProperty(max_length=5000)
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty()

    # 카드(Card)와 사용자(User) 간의 관계 정의
    owner = RelationshipFrom('USER', 'HAVE')

class HAS_RELATION(StructuredNode):
    relation_name = StringProperty(max_length=100)
    memo = StringProperty(max_length=100)
    delete_at = DateTimeProperty()
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty()

    # 사용자(User)와 다른 사용자(User) 간의 관계 정의
    user1 = RelationshipFrom('USER', 'HAS_RELATION')
    user2 = RelationshipTo('USER', 'HAS_RELATION')


# Relationships
# USER.cards = RelationshipTo(CARD, 'HAS_CARD')
# USER.relations = RelationshipTo(HAS_RELATION, 'HAS_RELATION')