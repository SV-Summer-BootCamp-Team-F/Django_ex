# backend/neo_db/urls.py
from django.urls import path
from .views import RegisterView, LoginView, UserInfoView, UserUpdateView, UpdateUserPhotoView, CardAddView, CardUpdateView, UserRelationView

urlpatterns = [
    path('api/v1/users/register/', RegisterView.as_view()),
    path('api/v1/users/login/', LoginView.as_view()),  # 추가한 줄
    path('api/v1/users/info/<str:user_uid>/', UserInfoView.as_view()),
    path('api/v1/users/update/', UserUpdateView.as_view()),
    path('api/v1/users/photo/<int:user_id>/', UpdateUserPhotoView.as_view()),  # <int:user_id> 부분에 실제 user_id를 넣습니다
    path('api/v1/cards/add/', CardAddView.as_view()),
    path('api/v1/cards/update/', CardUpdateView.as_view()),
    path('api/v1/relations/create/<int:user_id>/', UserRelationView.as_view(), name='create-relation'),
    #path('api/v1/relations/update/<int:user_id>/', UpdateRelationView.as_view(), name='update-relation'),
]
#