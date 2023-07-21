# neo_db/models.py
from neomodel import StructuredNode, StringProperty, BooleanProperty, DateProperty, UniqueIdProperty, RelationshipTo

class USER(StructuredNode):
    uid = UniqueIdProperty()
    user_name = StringProperty(unique_index=True, required=True)
    user_email = StringProperty(unique_index=True, required=True)
    password = StringProperty(required=True)
    phone_num = StringProperty(required=True)
    user_photo = StringProperty()
    is_user = BooleanProperty(default=True)
    created_at = DateProperty(auto_now_add=True)
    update_at = DateProperty(default_now=True)  # 이 줄 추가
    cards = RelationshipTo('CARD', 'HAS_CARD')


class CARD(StructuredNode):
    uid = UniqueIdProperty()
    card_name = StringProperty(unique_index=True, required=True)
    card_email = StringProperty(unique_index=True, required=True)
    card_intro = StringProperty()
    card_photo = StringProperty(required=True)
    created_at = DateProperty(auto_now_add=True)
    update_at = DateProperty(default_now=True)


class HAS_RELATION(StructuredNode):
    relation_name = StringProperty(max_length=100)
    memo = StringProperty(max_length=100)
    delete_at = DateProperty(auto_now_add=True)
    created_at = DateProperty(auto_now_add=True)
    update_at = DateProperty(auto_now_add=True)


