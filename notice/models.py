import os
from django.conf import settings
from django.db import models
from django.core.validators import MinLengthValidator
from .choice import *


class Employee(models.Model):
    # here
    emp_id = models.AutoField(primary_key=True, verbose_name="직원 사번번호이자 아이디")
    emp_name = models.CharField(max_length=10, verbose_name="직원 이름")
    emp_birth = models.DateField(verbose_name="생년월일")
    emp_gender = models.CharField(max_length=1, verbose_name="성별")
    emp_address = models.CharField(max_length=45, verbose_name="주소")
    emp_phone = models.CharField(max_length=45, verbose_name="핸드폰번호이자 비밀번호")
    emp_account = models.CharField(max_length=45, verbose_name="계좌번호")
    emp_email = models.EmailField(verbose_name="이메일")  # email
    emp_level = models.CharField(choices=LEVEL_CHOICES, max_length=1, default=1, verbose_name="접근 권한정보")
    emp_plus = models.IntegerField(default=0, verbose_name="추가 수당 정보")

    def __str__(self):
        return self.emp_name

class User(models.Model):
    # wrtie here
    user_email = models.EmailField(primary_key=True)  # email
    user_pw = models.CharField(validators=[MinLengthValidator(8)], max_length=10)  # min length
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column="emp_id")  # foreignkey

    def __str__(self):
        return self.user_email

class Notice(models.Model):
    # write here
    not_id = models.AutoField(primary_key=True)
    not_writer = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column="emp_email", verbose_name='작성자')
    not_title = models.CharField(max_length=128, verbose_name='제목')
    not_content = models.TextField(verbose_name='내용')
    not_hits = models.PositiveIntegerField(verbose_name='조회수', default=0)
    not_date = models.DateTimeField(auto_now_add=True,verbose_name='등록시간')

    def __str__(self):
        return self.not_title

    class Meta:
        db_table = '공지사항'
        verbose_name = '공지사항'
        verbose_name_plural = '공지사항'



