# backend/neo_db/urls.py
from django.urls import path
from .views import RegisterView, LoginView, UserInfoView, UserUpdateView, UpdateUserPhotoView, CardAddView, CardUpdateView ,UserRelationView, RelationView,RelationDeepView, CardDetailView,PhoneInfoView, CardInfoView
urlpatterns = [
    path('users/register/', RegisterView.as_view()),
    path('users/login/', LoginView.as_view()),  # 추가한 줄
    path('users/info/<str:user_uid>/', UserInfoView.as_view()),
    path('users/update/', UserUpdateView.as_view()),
    path('users/photo/<str:user_uid>/', UpdateUserPhotoView.as_view()),  # <int:user_id> 부분에 실제 user_id를 넣습니다
    path('cards/add/', CardAddView.as_view()),
    path('card/<str:card_uid>/', CardInfoView.as_view()),
    path('cards/update/', CardUpdateView.as_view()),
    path('relations/user', UserRelationView.as_view(), name='create-relation'),
    path('relations/first/<str:user_uid>/', RelationView.as_view()),
    path('relations/second/<str:user_uid>/', RelationDeepView.as_view()),
    path('relations/detail/<str:card_uid>/', CardDetailView.as_view(), name='card-detail'),
    path('relations/phone/<str:user_phone>/', PhoneInfoView.as_view()),
    #path('relations/nonuser', NonUserRegisterView.as_view(), name='nonuser-relation'),

]
#/relations/phone/{user_phone}