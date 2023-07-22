# neo_db/models.py
from neomodel import StructuredNode, StringProperty, BooleanProperty, DateProperty, UniqueIdProperty, RelationshipTo, RelationshipFrom

class USER(StructuredNode):
    uid = UniqueIdProperty()
    user_name = StringProperty(unique_index=True, required=True)
    user_email = StringProperty(unique_index=True, required=True)
    password = StringProperty(required=True)
    phone_num = StringProperty(required=True)
    user_photo = StringProperty()
    is_user = BooleanProperty(default=True)
    created_at = DateProperty(auto_now_add=True)
    update_at = DateProperty(default_now=True)
    cards = RelationshipTo('CARD', 'HAS_CARD')
    relations = RelationshipTo('HAS_RELATION', 'HAS_RELATION')

class CARD(StructuredNode):
    uid = UniqueIdProperty()
    card_name = StringProperty(unique_index=True, required=True)
    card_email = StringProperty(unique_index=True, required=True)
    card_intro = StringProperty()
    card_photo = StringProperty(required=True)
    created_at = DateProperty(auto_now_add=True)
    update_at = DateProperty(default_now=True)
    owners = RelationshipFrom('USER', 'HAS_CARD')
    relations = RelationshipFrom('HAS_RELATION', 'HAS_RELATION')

class HAS_RELATION(StructuredNode):
    relation_name = StringProperty(max_length=100)
    memo = StringProperty(max_length=100)
    delete_at = DateProperty(auto_now_add=True)
    created_at = DateProperty(auto_now_add=True)
    update_at = DateProperty(auto_now_add=True)
    user = RelationshipFrom('USER', 'HAS_RELATION')
    card = RelationshipTo('CARD', 'HAS_RELATION')
