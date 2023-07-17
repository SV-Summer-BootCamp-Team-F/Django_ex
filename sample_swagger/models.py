from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from backend import settings


class CustomUserManager(BaseUserManager):
#사용자 및 슈퍼사용자 생성을 처리하는 메소드
#아직 미완성!!!(매개변수 불충분)
    def create_user(self, email, password=None, **extra_fields):
        #이메일 주어지지 않을 경우 검사
        if not email:
            raise ValueError('The Email field must be set')
        #이메일 없을 경우 valueError를 발생
        #이메일 반드시 필요하다는 것을 알려주는 에러 메시지
        #email = self.normalize_email(email)
        #BaseUserManager 메소드 호출. 주어진 이메일 정규화 한다
        user = self.model(email=email, **extra_fields)
        #user 객체 생성. email 방금 정규화한 email 사용하고 추가적인 필드는 extra에서 가지고 옴
        user.set_password(password)
        #AbstractBaseUser 클래스 정의. raw password 해시하여 저장
        user.save(using=self._db)
        #데이터 베이스 객체 저장
        #using=self._db는 어디에 저장될 지 지정
        return user
#create_user 메소드는 email 및 password 입력으로 받고, 이를 사용하여 새로운 User 객체를 생성하고 저장
#User 객체를 생성하고 저장함.
    def create_superuser(self, email, password=None, **extra_fields):
        #email  와 password 필수 매개 변수로 전달
        #extra_fields 가변 키워드 매개변수 추가 필드에 대한 임의에 키워드 인수 받음
        extra_fields.setdefault('is_staff', True)
        #is_staff 사용자가 관리자인지 여부를 나타냄. 해당키 없을 경우 True 설정
        extra_fields.setdefault('is_superuser', True)
        #딕셔너리에서 is_superuser(최고 권한 사용자) 키를 검색하고 해당 키가 없을 경우 기본값을 true 설정
        return self.create_user(email, password, **extra_fields)
        #메소드 호출하여 슈퍼 유저 생성
        #extra_fields 딕셔너리의 키워드 인수를 풀어서 전달하는 구문
#User 객체를 생성하고 저장. create_superuser 메소드 create_user를 호출하되, is_staff

class User(AbstractBaseUser, PermissionsMixin):
    #Ab,Per 상속 받음
    #사용자 모델 커스텀하기 위해 Ab, 사용자 권환 관련 기능 PermissionMixin
    id = models.AutoField(primary_key=True)
    #AutoField 사용하여 기본 키로 설정
    user_name = models.CharField(max_length=255)
    user_email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone_num = models.CharField(max_length=20)
    user_photo = models.ImageField(upload_to='users/photos', blank=True, null=True)
    #user/photos 이미지 업로드 경로, 비었거나 선택적으로 선택 가능
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    delete_at = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()
    #CustomUserManager 객체를 object 속성 할당
    # 사용자 매니저 사용하여 사용자 모델을 관리

    USERNAME_FIELD = 'user_email'
    #사용자의 로그인 식별자로 사용할 필드 설정. 이메일로 설정
    REQUIRED_FIELDS = []
    #추가로 필요한 필드 없음 설정

    def __str__(self):
        return self.user_email
#객체를 문자열로 표현
# 사용자의 이메일 주소 반환

class Card(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #settings.AUTH_USER_MODEL는 사용자 모델와 관계 나타냄
    #사용자가 삭제되면 카드에도 삭제되게 casade 옵션을 사용
    card_name = models.CharField(max_length=200)
    card_email = models.EmailField(max_length=200)
    card_num = models.CharField(max_length=20)
    card_intro = models.TextField()
    card_photo = models.ImageField(upload_to='cards/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.card_name
# Create your models here.
