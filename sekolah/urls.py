from django.urls import include, path

from rest_framework import routers

from knox import views as knox_views

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
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls'), name='rest_framework'),
    path('api/', include(router.urls)),
    path('api/auth/login/', api.LoginView.as_view(), name='knox_login'),
    path('api/auth/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('api/auth/logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('api/auth/register/', api.RegisterView.as_view()),
]