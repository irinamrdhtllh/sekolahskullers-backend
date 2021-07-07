from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenViewBase

from . import serializers


class Register(TokenViewBase):
    serializer_class = serializers.TokenObtainPairSerializer

    def post(self, request, format=None):
        register_serializer = serializers.RegisterSerializer(data=request.data)
        register_serializer.is_valid(raise_exception=True)
        register_serializer.save()

        return super().post(request, format=format)


class Login(TokenViewBase):
    serializer_class = serializers.TokenObtainPairSerializer


class RefreshToken(TokenViewBase):
    serializer_class = serializers.TokenRefreshSerializer


class Logout(APIView):
    def post(self, *args, **kwargs):
        return Response({})
