# backend/neo_db/urls.py
from django.urls import path
from .views import RegisterView, LoginView, UserInfoView, UserUpdateView, UpdateUserPhotoView, CardAddView, CardUpdateView ,UserRelationView, RelationView,RelationDeepView, CardDetailView,PhoneInfoView
urlpatterns = [
    path('api/v1/users/register/', RegisterView.as_view()),
    path('api/v1/users/login/', LoginView.as_view()),  # 추가한 줄
    path('api/v1/users/info/<str:user_uid>/', UserInfoView.as_view()),
    path('api/v1/users/update/', UserUpdateView.as_view()),
    path('api/v1/users/photo/<str:user_uid>/', UpdateUserPhotoView.as_view()),  # <int:user_id> 부분에 실제 user_id를 넣습니다
    path('api/v1/cards/add/', CardAddView.as_view()),
    path('api/v1/cards/update/', CardUpdateView.as_view()),
    path('api/v1/relations/user', UserRelationView.as_view(), name='create-relation'),
    path('api/v1/relations/first/<str:user_uid>/', RelationView.as_view()),
    path('api/v1/relations/second/<str:user_uid>/', RelationDeepView.as_view()),
    path('api/v1/relations/detail/<str:card_uid>/', CardDetailView.as_view(), name='card-detail'),
    path('api/v1/relations/phone/<str:user_phone>/', PhoneInfoView.as_view()),
    #path('api/v1/relations/nonuser', NonUserRegisterView.as_view(), name='nonuser-relation'),

]
#/api/v1/relations/phone/{user_phone}