from django.urls import path

from management import views
from .views import list_employees, login

urlpatterns = [
    path('', views.list_wages, name='list_wages'),
    path("main/", views.list_schedule, name="list_schedule"),
    path('profile/', views.profile_view, name='profile'),
    path('profile_update/<int:emp_id>', views.profile_update_view, name='profile_update'),
    path('sta/', views.list_statement, name="list_statement"),
    path('emplist/', views.list_employees, name="list_employees"),
    path('empupdate/<int:id>/', views.update_employee, name='update_employee'),
    path('empcreate/',views.create_employee, name='create_employee'),
    path('schedule_exchange/', views.create_exchange, name='schedule_exchange'),
    path('schedule_substitution/', views.create_substitution, name='schedule_substitution'),
]