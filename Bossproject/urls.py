
from django.contrib import admin
from django.urls import path, include
import management.views
from django.views.generic import RedirectView

# login page로 고정
urlpatterns = [
    path("admin/", admin.site.urls),
    path('login/', management.views.login, name="login"),
    path('auth/', include('social_django.urls', namespace='social')),
    path("notice/",include('notice.urls')),
    path('mgmt/', include('management.urls')),

    ]
