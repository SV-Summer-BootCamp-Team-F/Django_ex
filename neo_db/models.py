# neo_db/models.py
from neomodel import StructuredNode, StringProperty, BooleanProperty, DateProperty, UniqueIdProperty

class User(StructuredNode):
    uid = UniqueIdProperty()
    user_name = StringProperty(unique_index=True, required=True)
    user_email = StringProperty(unique_index=True, required=True)
    password = StringProperty(required=True)
    phone_num = StringProperty(required=True)
    user_photo = StringProperty()
    is_user = BooleanProperty(default=True)
    created_at = DateProperty(auto_now_add=True)
#알