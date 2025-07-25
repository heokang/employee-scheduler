from django.urls import path
from notice import views

urlpatterns = [
    path('', views.NoticeListView.as_view(), name='notice_list'),
    path('<int:pk>/', views.notice_detail_view, name='notice_detail'),
    path('write/', views.notice_write_view, name='notice_write'),
    path('<int:pk>/edit/', views.notice_edit_view, name='notice_edit'),
    path('<int:pk>/delete/', views.notice_delete_view, name='notice_delete'),

]