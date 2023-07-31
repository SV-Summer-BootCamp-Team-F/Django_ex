# backend/neo_db/urls.py
from django.urls import path
from django.conf import settings  # 이하를 추가
from django.conf.urls.static import static
from .views import RegisterView, LoginView, UserInfoView, UserUpdateView, UpdateUserPhotoView, CardAddView, CardUpdateView ,UserRelationView, AllRelationView, CardDetailView,PhoneInfoView, CardInfoView, UpdateCardPhotoView


urlpatterns = [
    # 차례대로 회원가입 , 로그인
    path('users/register/', RegisterView.as_view()),
    path('users/login/', LoginView.as_view()),  # 추가한 줄

    # 유저 정보 불러오기 , 유저 정보 수정 , 유저 프로필 사진 수정
    path('users/info/<str:user_uid>/', UserInfoView.as_view()),
    path('users/update/<str:user_uid>/', UserUpdateView.as_view()),
    path('users/photo/<str:user_uid>/', UpdateUserPhotoView.as_view()),  # <int:user_id> 부분에 실제 user_id를 넣습니다

    # 명함 등록 , 명함 정보 불러오기 ,명함 정보 수정, 명함 프로필 사진 수정
    path('cards/add/<str:user_uid>/', CardAddView.as_view()),
    path('cards/info/<str:user_uid>/', CardInfoView.as_view()),
    path('cards/update/<str:user_uid>/', CardUpdateView.as_view()),
    path('cards/photo/<str:user_uid>/', UpdateCardPhotoView.as_view()),  # <int:user_id> 부분에 실제 user_id를 넣습니다

    # 유저 관계 연결 , 관계 전체 보기 , 명함 관계 상세 보기 , 번호 조회하기
    path('relations/user/<str:user_uid>/', UserRelationView.as_view(), name='create-relation'),
    path('relations/all/<str:user_uid>/', AllRelationView.as_view()),
    path('relations/detail/<str:card_uid>/', CardDetailView.as_view(), name='card-detail'),
    path('relations/phone/<str:card_phone>/', PhoneInfoView.as_view()),
    #path('relations/nonuser', NonUserRegisterView.as_view(), name='nonuser-relation'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#/relations/phone/{user_phone}
#media : 사용자가 웹에 업로드한 파일
#static : 개발 단계에서 업로드해서 보여주는 파일. default image
#/relations/phone/{user_phone}
