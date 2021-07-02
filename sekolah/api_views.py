from rest_framework import permissions, generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Student, Group, ClassYear
from .serializers import (
    RegisterSerializer,
    StudentSerializer,
    GroupSerializer,
    ClassYearSerializer,
)


@api_view(['GET'])
def api_root(request, format=None):
    return Response(
        {
            'register': reverse('register', request=request, format=format),
            'token_obtain_pair': reverse(
                'token_obtain_pair', request=request, format=format
            ),
            'token_refresh': reverse('token_refresh', request=request, format=format),
            'students': reverse('students', request=request, format=format),
            'groups': reverse('groups', request=request, format=format),
            'class-year': reverse('class_year', request=request, format=format),
            'profile': reverse('profile', request=request, format=format),
            'group_profile': reverse('group_profile', request=request, format=format),
        }
    )


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        )


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
