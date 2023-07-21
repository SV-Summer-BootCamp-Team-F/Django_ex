"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# backend/urls.py

# backend/urls.py
from rest_framework import permissions
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(                  #  API 스키마를 만들기 위한 뷰를 생성하는 데 사용,Swagger UI와 연동되어 API 문서를 제공하고 시각적으로 보여줌
    openapi.Info(                               #  API의 기본 정보를 설정
        title="remember+ API",
        default_version='v1',
        description="remember+ API 문서",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="kawy.sojung@gmail.com"),
        license=openapi.License(name="kawksojung"),
    ),
    public=True,                                #  API 스키마가 공개되도록 설정
    permission_classes=[permissions.AllowAny],  #  누구나 API 스키마를 조회할 수 있도록 허용
)

urlpatterns = [
    path('admin/', admin.site.urls),             # 관리자 사이트에 대한 URL 패턴
    path('', include('neo_db.urls')),            # 빈경로 URL 패턴으로, neo_db.urls로 시작하는 URL을 include합니다. 이는 neo_db 애플리케이션의 URL 설정을 추가하라는 의미
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'), # swagger UI의 JSON 또는 YAML 스키마를 조회하기 위한 URL
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),                 #  /swagger/ 경로에 대한 URL 패턴으로, Swagger UI를 사용하여 API 스키마를 조회
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # Redoc UI를 사용하여 API 스키마를 조회할 수 있도록 설정
    path('USER/', include('neo_db.urls'))   #neo_db.urls로 시작하는 URL을 include,  /USER/ 경로를 처리하기 위해 해당 애플리케이션의 URL 설정을 추가하라는 의미
]

#