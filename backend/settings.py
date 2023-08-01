"""
Django settings for django_ex project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

from neomodel import config
config.MAX_POOL_SIZE = 50

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ei+d5(j38wpe9abp-nnc3q^sjc+!5bzs-$i=n!-9jj22gem$#w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#스웨거가 있는데 이거 뭘까요 -재민

SWAGGER_SETTINGS = {
   'USE_SESSION_AUTH': True
}
ALLOWED_HOSTS = ['*']

APPEND_SLASH=False

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', #swagger ui의 css,js 파일 제공하기 위해 필요한 장고 앱
    'drf_yasg', #swagger  연동을 위해서 ISATALL
    'django_neomodel', # neo4j연동에 필요
    'rest_framework', #장고 연동을 위한 필요
    'neo_db.apps.Neo_dbConfig', #이건 neo4j?
    #'neo4django',
    'corsheaders',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.AdminRenderer',
    ]
}


# # Neo4j 데이터베이스 설정
# NEO4J_BOLT_URL = os.environ.get('NEO4J_BOLT_URL', 'bolt://neo4j:123412341234@container_neo4j:7689')
DATABASE_URL = "bolt://user:password@container_neo4j:7687"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}

NEO4J_BOLT_URL = 'bolt://container_neo4j:7687'
NEO4J_USERNAME = 'neo4j'
NEO4J_PASSWORD = '123412341234'


NEOMODEL_SIGNALS = True
NEOMODEL_FORCE_TIMEZONE = False
NEOMODEL_ENCRYPTED_CONNECTION = True
NEOMODEL_MAX_POOL_SIZE = 50

#swwagger_setting 을 위한 연동
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'bootcamp',
            'in': 'header'
        }
    },
}

##CORS
CORS_ORIGIN_ALLOW_ALL=True # <- 모든 호스트 허용
CORS_ALLOW_CREDENTIALS = True # <-쿠키가 cross-site HTTP 요청에 포함될 수 있다

#이것도 확인
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATIC_URL = '/static/'
#실제 경로 아닌 파일이 접근 할 수 있게 url 주기 위한 기본적인 베이스

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',

        'NAME':  os.path.join(BASE_DIR , 'db.sqlite3'),  # os.path.join, 확인해야함
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'


USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

#STATIC_URL = '/static/'
#프로젝트 이미 정해져 있는 파일, 개발할 때 이미 준비되어진 파일
#웹 사이트에서 static파일을 참조할 때 사용하는 url 설정
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
#static 파일들 저장될 디렉토리의 경로를 설정
#static 이라는 디렉토리 파일에 staitc 파일을 저장할 예정

# Base Directory의 static 폴더
STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = 'static/'

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

STATICFILES_DIRS=[
    os.path.join(BASE_DIR,'neo_db','static')
] #static 파일들이 어디에 있는지를 쓰는곳

#Django 개발 서버: STATICFILES_DIR
#웹 서버: STATIC_ROOT

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
