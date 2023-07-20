from django.urls import path
from .views import RegisterView

urlpatterns = [
    path('api/v1/users/register/', RegisterView.as_view()),
]