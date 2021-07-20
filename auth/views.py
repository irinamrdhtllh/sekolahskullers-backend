from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenViewBase

from . import serializers


class RegisterView(TokenViewBase):
    serializer_class = serializers.LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        register_serializer = serializers.RegisterSerializer(data=request.data)
        register_serializer.is_valid(raise_exception=True)
        user = register_serializer.save()

        request.user = user
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


class LoginView(TokenViewBase):
    serializer_class = serializers.LoginSerializer
    permission_classes = [permissions.AllowAny]


class RefreshTokenView(TokenViewBase):
    serializer_class = serializers.RefreshTokenSerializer
    permission_classes = [permissions.AllowAny]


class PasswordResetView(GenericAPIView):
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'detail': 'Password reset email has been sent',
            }
        )


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = serializers.PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'detail': 'Password has been reset successfully',
            }
        )
