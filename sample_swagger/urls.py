from django.conf.urls import url,include
from django.contrib import admin
from rest_framework import routers
from sample_swagger.views import UserViewSet
router = routers.DefaultRouter()
router.register('users', UserViewSet)  # 'User'를 'users'로 변경

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^',include('router.urls')),
]
