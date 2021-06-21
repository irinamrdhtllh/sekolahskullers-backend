from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('year/', views.year, name='year'),
    path('group/', views.group, name='group'),
    path('student/', views.student, name='student'),
    path('accounts/register/', views.register, name='register'),
    path('upload/', views.upload),
]
