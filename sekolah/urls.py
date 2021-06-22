from django import urls
from django.urls import path
from django.urls.conf import include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),
    path('year/', views.year, name='year'),
    path('group/', views.group, name='group'),
    path('student/', views.student, name='student'),
    path('upload/', views.upload),
]
