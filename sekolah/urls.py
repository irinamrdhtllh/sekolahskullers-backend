from django.urls import include, path

from knox import views as knox_views

from . import views, api


urlpatterns = [
    path('', views.home, name='home'),
    path('upload/<action>/', views.upload),
]

urlpatterns += [
    path('api/register/', api.RegisterView.as_view(), name='register'),
    path('api/login/', api.LoginView.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutAllView.as_view(), name='logout'),
    path('api/students/', api.StudentView.as_view(), name='students'),
    path('api/groups/', api.GroupView.as_view(), name='groups'),
    # path('api/year/', api.YearView.as_view(), name='year'),
    path('api/auth/profile/', api.ProfileView.as_view(), name='profile'),
    path(
        'api/auth/profile/group/', api.GroupProfileView.as_view(), name='group_profile'
    ),
    path('api-auth/', include('rest_framework.urls')),
]
