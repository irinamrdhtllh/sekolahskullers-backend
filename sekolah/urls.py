from django.urls import include, path
from django.views.generic.base import RedirectView

from . import views, api_views, auth_views

urlpatterns = [
    path('', RedirectView.as_view(url='api/')),
    path('api-auth/', include('rest_framework.urls')),
    path('upload/<action>/', views.upload),
]

# API views
urlpatterns += [
    path('api/', api_views.api_root, name='api_root'),
    path('api/students/', api_views.StudentView.as_view(), name='students'),
    path('api/groups/', api_views.GroupView.as_view(), name='groups'),
    path('api/class-year/', api_views.ClassYearView.as_view(), name='class_year'),
    path('api/profile/', api_views.ProfileView.as_view(), name='profile'),
    path(
        'api/profile/group/', api_views.GroupProfileView.as_view(), name='group_profile'
    ),
]

# Auth views
urlpatterns += [
    path('api/register/', auth_views.Register.as_view(), name='register'),
    path('api/token/', auth_views.Login.as_view(), name='login'),
    path('api/token/refresh/', auth_views.RefreshToken.as_view(), name='refresh'),
    path('api/token/logout/', auth_views.Logout.as_view(), name='logout'),
]
