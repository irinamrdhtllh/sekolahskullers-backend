from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.reverse import reverse

from . import models, serializers


@api_view(['GET'])
def api_root(request, format=None):
    return Response(
        {
            'students': reverse('students', request=request, format=format),
            'groups': reverse('groups', request=request, format=format),
            'class-year': reverse('class_year', request=request, format=format),
            'profile': reverse('profile', request=request, format=format),
            'group_profile': reverse('group_profile', request=request, format=format),
            'shop': reverse('shop', request=request, format=format),
        }
    )


class StudentView(generics.ListAPIView):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    permission_classes = [permissions.AllowAny]


class GroupView(generics.ListAPIView):
    queryset = models.Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = [permissions.AllowAny]


class ClassYearView(generics.RetrieveAPIView):
    serializer_class = serializers.ClassYearSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return models.ClassYear.objects.first()


class ProfileView(generics.RetrieveAPIView):
    serializer_class = serializers.StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.student


class GroupProfileView(generics.RetrieveAPIView):
    serializer_class = serializers.GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        group = self.request.user.student.group

        if group:
            return group

        raise ValidationError({'group': ['No group available.']})


class ShopView(generics.GenericAPIView):
    serializer_class = serializers.ShopSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.student

    def patch(self, request, format=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'detail': 'Operation completed successfully.'})
