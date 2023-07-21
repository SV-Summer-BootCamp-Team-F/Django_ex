# backend/neo_db/urls.py
from django.urls import path
from .views import RegisterView, LoginView

urlpatterns = [
    path('api/v1/users/register/', RegisterView.as_view()),
    path('api/v1/users/login/', LoginView.as_view()),  # 추가한 줄
]
#