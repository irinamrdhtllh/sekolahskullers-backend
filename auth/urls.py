from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('token/', views.LoginView.as_view(), name='login'),
    path('token/refresh/', views.RefreshTokenView.as_view(), name='refresh'),
    path(
        'password/reset/',
        views.PasswordResetView.as_view(),
        name='password_reset',
    ),
    path(
        'password/reset/confirm/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
]
