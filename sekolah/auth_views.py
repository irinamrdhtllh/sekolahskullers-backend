from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import TokenViewBase

from . import auth_serializers


class Register(TokenViewBase):
    serializer_class = auth_serializers.TokenObtainPairSerializer

    def post(self, request, format=None):
        register_serializer = auth_serializers.RegisterSerializer(data=request.data)
        register_serializer.is_valid(raise_exception=True)
        register_serializer.save()

        return super().post(request, format=format)


class Login(TokenViewBase):
    serializer_class = auth_serializers.TokenObtainPairSerializer


class RefreshToken(TokenViewBase):
    serializer_class = auth_serializers.TokenRefreshSerializer


class Logout(APIView):
    def post(self, *args, **kwargs):
        return Response({})


class PasswordResetView(GenericAPIView):
    serializer_class = auth_serializers.PasswordResetSerializer
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


class PasswordResetConfirm(GenericAPIView):
    serializer_class = auth_serializers.PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'detail': 'Password has been reset with the new password',
            }
        )
