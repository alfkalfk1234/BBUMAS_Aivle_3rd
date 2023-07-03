from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
class CustomUser(AbstractUser):
    # 기존의 email 필드를 필수로 변경
    email = models.EmailField(blank=False, null=False)

    # special 필드 추가 (default value = False)
    special = models.BooleanField(default=False)

    # phone 필드 추가
    phone = models.CharField(max_length=20, blank=False, null=False)

    # first_name과 last_name을 선택적으로 변경
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)

    # name 필드 추가
    name = models.CharField(max_length=150, blank=False, null=False)

    region = models.CharField(max_length=150, blank=False, null=False, default=' ')

