from django.urls import include, path

from rest_framework_simplejwt.views import token_obtain_pair, token_refresh

from . import views, api_views


urlpatterns = [
    path('', api_views.api_root, name='api_root'),
    path('api/register/', api_views.RegisterView.as_view(), name='register'),
    path('api/token/', token_obtain_pair, name='token_obtain_pair'),
    path('api/token/refresh/', token_refresh, name='token_refresh'),
    path('api/students/', api_views.StudentView.as_view(), name='students'),
    path('api/groups/', api_views.GroupView.as_view(), name='groups'),
    path('api/class-year/', api_views.ClassYearView.as_view(), name='class_year'),
    path('api/auth/profile/', api_views.ProfileView.as_view(), name='profile'),
    path(
        'api/auth/profile/group/',
        api_views.GroupProfileView.as_view(),
        name='group_profile'
    ),
    path('api-auth/', include('rest_framework.urls')),
    path('upload/<action>/', views.upload),
]
