from django.db import models

from backend import settings


class Users(models.Model):
    user_email = models.CharField(max_length=30)  # 제목
    user_name = models.CharField(max_length=100)  # 내용
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delete_at = models.DateTimeField(blank=True, null=True)

def __str__(self):
    return self.user_email


#객체를 문자열로 표현
# 사용자의 이메일 주소 반환
