from django.contrib.auth import login

from rest_framework import permissions, generics
from rest_framework.authtoken.serializers import AuthTokenSerializer

from knox.views import LoginView as KnoxLoginView

from .models import Student, Group, ClassYear
from .serializers import (
    RegisterSerializer,
    StudentSerializer,
    GroupSerializer,
    ClassYearSerializer,
)


class LoginView(KnoxLoginView):
    permission_classes = [permissions.AllowAny]

    def get_post_response_data(self, request, token, instance):
        data = {
            'student': StudentSerializer(
                request.user.student, context=self.get_context()
            ).data,
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token,
        }
        return data

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=None)


class RegisterView(KnoxLoginView):
    permission_classes = [permissions.AllowAny]

    def get_post_response_data(self, request, token, instance):
        data = {
            'student': StudentSerializer(
                request.user.student, context=self.get_context()
            ).data,
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token,
        }
        return data

    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        return super().post(request, format=None)


class StudentView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.AllowAny]


class GroupView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.AllowAny]


class ClassYearView(generics.RetrieveAPIView):
    serializer_class = ClassYearSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return ClassYear.objects.get(pk=1)


class ProfileView(generics.RetrieveAPIView):
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.student


class GroupProfileView(generics.RetrieveAPIView):
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.student.group
