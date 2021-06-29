from django.urls import include, path

from knox import views as knox_views

from . import views, api_views


urlpatterns = [
    path('', views.home, name='home'),
    path('upload/<action>/', views.upload),
]

urlpatterns += [
    path('api/register/', api_views.RegisterView.as_view(), name='register'),
    path('api/login/', api_views.LoginView.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutAllView.as_view(), name='logout'),
    path('api/students/', api_views.StudentView.as_view(), name='students'),
    path('api/groups/', api_views.GroupView.as_view(), name='groups'),
    path('api/class-year/', api_views.ClassYearView.as_view(), name='class_year'),
    path('api/auth/profile/', api_views.ProfileView.as_view(), name='profile'),
    path(
        'api/auth/profile/group/', api_views.GroupProfileView.as_view(), name='group_profile'
    ),
    path('api-auth/', include('rest_framework.urls')),
]
