from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import TokenViewBase

from . import serializers


class RegisterView(TokenViewBase):
    serializer_class = serializers.LoginSerializer

    def post(self, request, format=None):
        register_serializer = serializers.RegisterSerializer(data=request.data)
        register_serializer.is_valid(raise_exception=True)
        register_serializer.save()

        return super().post(request, format=format)


class LoginView(TokenViewBase):
    serializer_class = serializers.LoginSerializer


class RefreshTokenView(TokenViewBase):
    serializer_class = serializers.RefreshTokenSerializer


class PasswordResetView(GenericAPIView):
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'detail': 'Password reset email has been sent',
            },
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = serializers.PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'detail': 'Password has been reset successfully',
            }
        )
