from django.conf import settings
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework_simplejwt import serializers as jwt_serializers
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.tokens import RefreshToken

from . import models


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=128, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'password2',
        ]
        write_only_fields = ['password', 'password2']

    def validate(self, data):
        password1 = data['password']
        password2 = data.pop('password2')
        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError({'password': 'Password doesn\'t match'})
        return super().validate(data)

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        models.Student.objects.create(user=user)
        return user


class TokenObtainPairSerializer(jwt_serializers.TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Custom claims
        token["username"] = user.get_username()

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['refresh_expires'] = refresh["exp"]
        data['access'] = str(refresh.access_token)
        data['access_expires'] = refresh.access_token["exp"]

        return data


class TokenRefreshSerializer(serializers.Serializer):
    # Instead of inputting the refresh token from the HTTP body, we pull it
    # from the cookie

    def get_token_from_cookie(self):
        request = self.context["request"]
        return request.COOKIES.get(settings.JWT_COOKIE_NAME)

    def validate(self, attrs):
        token = self.get_token_from_cookie()
        if token is None:
            raise serializers.ValidationError("No refresh token cookie found")
        refresh = RefreshToken(token)

        data = {
            "access": str(refresh.access_token),
            "access_expires": refresh.access_token["exp"],
        }

        if jwt_settings.BLACKLIST_AFTER_ROTATION:
            try:
                # Attempt to blacklist the given refresh token
                refresh.blacklist()
            except AttributeError:
                # If blacklist app not installed, `blacklist` method will
                # not be present
                pass

        refresh.set_jti()
        refresh.set_exp()

        data['refresh'] = str(refresh)
        data['refresh_expires'] = refresh["exp"]

        return data


class StudentTaskStatusSerializer(serializers.ModelSerializer):
    task = serializers.StringRelatedField()
    is_required = serializers.BooleanField(source='task.is_required')
    deadline = serializers.DateTimeField(source='task.deadline')
    max_score = serializers.IntegerField(source='task.max_score')
    link = serializers.CharField(source='task.link')

    class Meta:
        model = models.StudentTaskStatus
        fields = [
            'task',
            'is_complete',
            'score',
            'is_required',
            'deadline',
            'max_score',
            'link',
        ]


class AssessmentField(serializers.Field):
    def to_representation(self, value):
        return {
            'kepemimpinan': value.assessment1,
            'keteknikfisikaan': value.assessment2,
            'kemahasiswaan': value.assessment3,
            'solidaritas': value.assessment4,
            'kolaboratif': value.assessment5,
            'semangatMenjelajah': value.assessment6,
            'semangatMemaknai': value.assessment7,
        }


class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    group = serializers.StringRelatedField()
    task_statuses = StudentTaskStatusSerializer(many=True)
    assessment = AssessmentField(read_only=True)

    class Meta:
        model = models.Student
        fields = [
            'username',
            'first_name',
            'last_name',
            'health',
            'exp',
            'level',
            'assessment',
            'task_statuses',
            'group',
        ]


class GroupTaskStatusSerializer(serializers.ModelSerializer):
    task = serializers.StringRelatedField()
    is_required = serializers.BooleanField(source='task.is_required')
    deadline = serializers.DateTimeField(source='task.deadline')
    max_score = serializers.IntegerField(source='task.max_score')
    link = serializers.CharField(source='task.link')

    class Meta:
        model = models.GroupTaskStatus
        fields = [
            'task',
            'is_complete',
            'score',
            'is_required',
            'deadline',
            'max_score',
            'link',
        ]


class GroupSerializer(serializers.ModelSerializer):
    task_statuses = GroupTaskStatusSerializer(many=True)
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = models.Group
        fields = ['name', 'health', 'exp', 'level', 'task_statuses', 'students']


class ClassYearTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClassYearTask
        fields = [
            'name',
            'is_complete',
            'score',
            'is_required',
            'deadline',
            'max_score',
            'link',
        ]


class MissionField(serializers.RelatedField):
    def to_representation(self, value):
        return value.text


class ClassYearSerializer(serializers.ModelSerializer):
    tasks = ClassYearTaskSerializer(many=True, read_only=True)
    missions = MissionField(many=True, read_only=True)

    class Meta:
        model = models.ClassYear
        fields = ['name', 'health', 'exp', 'level', 'vision', 'missions', 'tasks']
