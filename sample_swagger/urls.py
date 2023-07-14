from django.urls import path
from myapp.views import MyAPIView

from django.urls import path
from . import views

app_name='sample_swagger'
urlpatterns = [
    path('/get_url',views.get, name = 'get'),
    path('/post_url',views.post, name = 'post'),
]

