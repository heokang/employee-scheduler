from django.contrib.auth import authenticate
from django.shortcuts import render
from datetime import datetime

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from pyexpat.errors import messages # 추가한거니깐 확인

from .decorators import login_message_required
# Create your views here.
from .models import Wage_hourly, Absenteeism, Employee, Schedule_exchange
from django.db.models import Sum
from datetime import datetime
from .form import EmployeeForm,ExchangeForm
from .form import CustomCsUserChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount



def list_wages(request):
    wages = Wage_hourly.objects.all()
    return render(request, 'wages/list_wages.html', {'wages': wages})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('list_schedule')  # 로그인 성공 시 list_employees 페이지로 리디렉션
        else:
            # 인증 실패 처리
            return render(request, 'login.html', {'error': '잘못된 자격 증명입니다.'})
    return render(request, 'login.html')


# 알바생 메인화면 스케줄표 (개인화면이 아닌 알바생 모두가 같은 화면), 로그인하면 바로 여기로 넘어감
def list_schedule(request):
    return render(request, 'schedule/list__schedule.html')


@login_required
def profile_view(request):
    user = request.user
    if user.username == 'boss':
        employees = Employee.objects.all()  # Get all employees' information
    else:
        email = user.email
        employees = Employee.objects.filter(emp_email=email)

    return render(request, 'employee/profile.html', {'employees': employees})


@login_required
def profile_update_view(request, emp_id):
    employee = Employee.objects.get(emp_id=emp_id)
    emp_change_form = CustomCsUserChangeForm(request.POST or None, instance=employee)

    if request.method == 'POST':
        emp_change_form = CustomCsUserChangeForm(request.POST, instance=employee)
        if emp_change_form.is_valid():
            emp_change_form.save()
            return redirect('profile')

    return render(request, 'employee/profile_update.html', {'employee': employee, 'emp_change_form': emp_change_form})

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')

def list_employees(request):
    employees = Employee.objects.all()
    return render(request, 'employee/list_employees.html', {'employees': employees})


def create_employee(request):
    form = EmployeeForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('list_employees')

    return render(request, 'management/employee_form.html', {'form': form})


def update_employee(request, id):
    employee = Employee.objects.get(emp_id=id)
    form = EmployeeForm(request.POST or None, instance=employee)

    return render(request, 'management/employee_form.html', {'emp': employee, 'form': form})


def list_statement(request):
    month = request.GET.get('month')
    year = request.GET.get('year')

    if not year:
        year = datetime.now().year
    if month and year:
        message = f'{year}년 {month}월 명세서'
        lists = Absenteeism.objects.filter(abs_start__year=year, abs_start__month=month)
    else:
        message = '월을 입력하세요.'
        lists = Absenteeism.objects.order_by('employee')

    total = lists.aggregate(total_sum=Sum('abs_totalmin'), total_wage=Sum('abs_totalwage'))

    def convert_to_hours_minutes(total_minutes):
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f'{hours}시간 {minutes}분'

    context = {
        'message': message,
        'lists': lists,
        'total_sum': convert_to_hours_minutes(total['total_sum']),
        'total_wage': total['total_wage']
    }
    return render(request, "statement/list_statement.html", context)

# def register_worktime(request):
#     form = UserForm(request.POST or None)
#
#     if form.is_valid():
#         form.save()
#         return redirect('Absenteeism')
#
#     return render(request, 'management/login.html', {'form': form})

#피신청자 시간이 비어있으면 오류
@login_required
def create_exchange(request):
    user = request.user
    email = user.email
    employee1 = Employee.objects.get(emp_email=email)


    if request.method == 'POST':
        form = ExchangeForm(employee1,request.POST)


        if form.is_valid():
            schedule_exchange = form.save(commit=False)
            schedule_exchange.employee1 = employee1
            schedule_exchange.save()
            return redirect('schedule_exchange')

    else:
        form = ExchangeForm(employee1)

    context = {
        'form': form,
    }
    return render(request, 'schedule/schedule_exchange_form.html', context)

# 피신청자 시간이 비어있어야함
@login_required
def create_substitution(request):
    user = request.user
    email = user.email
    employee1 = Employee.objects.get(emp_email=email)

    if request.method == 'POST':
        form = ExchangeForm(employee1,request.POST)

        if form.is_valid():
            schedule_exchange = form.save(commit=False)
            schedule_exchange.employee1 = employee1
            schedule_exchange.save()
            return redirect('schedule_exchange')

    else:
        form = ExchangeForm(employee1)

    context = {
        'form': form,
    }
    return render(request, 'schedule/schedule_exchange_form.html', context)