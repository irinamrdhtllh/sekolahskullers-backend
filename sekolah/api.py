from django.contrib.auth import login

from rest_framework import viewsets, permissions, generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response

from knox.auth import TokenAuthentication
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView

from .models import Student
from .serializers import RegisterSerializer, StudentSerializer


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    lookup_field = 'user__username'


class LoginView(KnoxLoginView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=None)


class RegisterView(generics.GenericAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        return Response(
            {
                'student': StudentSerializer(
                    user.student, context=self.get_serializer_context()
                ).data,
                'token': AuthToken.objects.create(user)[1],
            }
        )
