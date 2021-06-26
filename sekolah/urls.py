from django.urls import include, path

from rest_framework import routers

from . import views, api

router = routers.DefaultRouter()
router.register(r'students', api.StudentViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),
    path('year/', views.year, name='year'),
    path('group/', views.group, name='group'),
    path('student/', views.student, name='student'),
    path('upload/<action>/', views.upload),
    path('api/', include(router.urls)),
    path('api/auth/register/', api.register),
    path('api/auth/login/', api.login),
    path('api-auth/', include('rest_framework.urls'), name='rest_framework'),
]
