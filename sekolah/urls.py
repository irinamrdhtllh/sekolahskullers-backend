from django.urls import path

from . import views, upload_views

# Upload view
urlpatterns = [
    path('upload/', upload_views.upload, name='upload'),
    path('upload/<action>/', upload_views.upload),
]

# API views
urlpatterns += [
    path('', views.api_root, name='api_root'),
    path('students/', views.StudentView.as_view(), name='students'),
    path('groups/', views.GroupView.as_view(), name='groups'),
    path('class-year/', views.ClassYearView.as_view(), name='class_year'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile-group/', views.GroupProfileView.as_view(), name='group_profile'),
]
