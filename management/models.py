from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.utils.functional import cached_property
from .choice import *
import datetime

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
    emp_level = models.CharField(choices=LEVEL_CHOICES,max_length=1, default=1, verbose_name="접근 권한정보")
    emp_plus = models.IntegerField(default=0, verbose_name="추가 수당 정보")

    def __str__(self):
        return self.emp_name


class Schedulefix(models.Model):
    # here
    sch_id = models.AutoField(primary_key=True)
    sch_start = models.DateTimeField()
    sch_finish = models.DateTimeField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column="emp_id")

    def __str__(self):
        return str(self.sch_date)

# 대타를 위해 피신청자 time null 값 허용으로 변경
class Schedule_exchange(models.Model):
    # write here
    employee1 = models.ForeignKey(Employee, related_name="exchange_employee1", on_delete=models.CASCADE,db_column="emp_id1")
    employee2 = models.ForeignKey(Employee, related_name="exchange_employee2", on_delete=models.CASCADE,db_column="emp_id2")
    start1 = models.DateTimeField(null=True)
    end1 = models.DateTimeField(null=True)
    start2 = models.DateTimeField()
    end2 = models.DateTimeField()


class Wage_hourly(models.Model):
    # write here
    wag_id = models.AutoField(primary_key=True)
    wag_info = models.CharField(max_length=10)
    wag_price = models.IntegerField(default=0)

    def __str__(self):
        return self.wag_info


class Absenteeism(models.Model):
    # wrtie here
    abs_id = models.AutoField(primary_key=True)
    abs_start = models.DateTimeField()
    abs_finish = models.DateTimeField()
    abs_totalmin = models.IntegerField(default=0)
    abs_totalwage = models.IntegerField(default=0)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column="emp_id")
    wageinfo = models.ForeignKey(Wage_hourly, on_delete=models.CASCADE, db_column="wag_id")

    def calculate_totalhour(self):
        time_difference = self.abs_finish - self.abs_start
        self.abs_totalmin = int(time_difference.total_seconds() / 60)

    def calculate_totalwage(self):
        wage_price = self.wageinfo.wag_price +self.employee.emp_plus
        self.abs_totalwage = int(self.abs_totalmin * (wage_price/60))

    def save(self, *args, **kwargs):
        self.calculate_totalhour()
        self.calculate_totalwage()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.employee)


