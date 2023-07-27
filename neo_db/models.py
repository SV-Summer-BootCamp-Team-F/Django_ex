from neomodel import StructuredNode, StringProperty, BooleanProperty, DateProperty, UniqueIdProperty, RelationshipTo, \
    RelationshipFrom, DateTimeProperty, StructuredRel

class HAVE(StructuredRel):
    uid = UniqueIdProperty()
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)

class RELATION(StructuredRel):
    relatoion_uid = StringProperty()  # UUID는 문자열로 저장됩니다.(이름 변경)
    relation_name = StringProperty(required=True)
    memo = StringProperty()
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)

class USER(StructuredNode):
    user_uid = StringProperty(required=False)  #그냥 추가
    user_name = StringProperty(unique_index=True, required=True)
    user_email = StringProperty(unique_index=True, required=True)
    password = StringProperty(required=True)
    user_phone = StringProperty(required=True,unique_index=True)
    user_photo = StringProperty()
    is_user = BooleanProperty(default=True)
    created_at = DateProperty(auto_now_add=True)
    update_at = DateProperty(default_now=True)
    cards = RelationshipTo('CARD', 'HAVE', model=HAVE)
    relations = RelationshipTo('USER', 'RELATION', model=RELATION)  # Use this line only

class CARD(StructuredNode):
    card_uid = StringProperty(required=False) #추가
    card_name = StringProperty(unique_index=True, required=True)
    card_email = StringProperty(unique_index=True, required=True)
    card_phone = StringProperty(required=True)
    card_intro = StringProperty()
    card_photo = StringProperty(required=True)
    created_at = DateProperty(auto_now_add=True)
    update_at = DateProperty(default_now=True)
    owners = RelationshipFrom('USER', 'HAVE', model=HAVE)


