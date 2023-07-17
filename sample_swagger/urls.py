from django.urls import path
from .views import UserList, UserDetail
from .views import CardCreate, CardList, CardRetrieve, CardUpdate, CardDelete

urlpatterns = [
    path('Users/', UserList.as_view(), name='user_list'),
    path('User/',UserDetail.as_view(),name='User_create'),
    path('User/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('card/', CardCreate.as_view(), name='card_create'),
    path('cards/', CardList.as_view(), name='card_list'),
    path('card/<int:pk>/', CardRetrieve.as_view(), name='card_retrieve'),
    path('card/<int:pk>/update/', CardUpdate.as_view(), name='card_update'),
    path('card/<int:pk>/delete/', CardDelete.as_view(), name='card_delete'),
]