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
        token['username'] = user.get_username()

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['refresh_expires'] = refresh['exp']
        data['access'] = str(refresh.access_token)
        data['access_expires'] = refresh.access_token['exp']

        return data


class TokenRefreshSerializer(jwt_serializers.TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])

        data = super().validate(attrs)
        data['access_expires'] = refresh.access_token['exp']

        return data


class LevelField(serializers.ChoiceField):
    def to_representation(self, value):
        return {'value': value, 'display': self.grouped_choices[value]}


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
            'semangat_menjelajah': value.assessment6,
            'semangat_memaknai': value.assessment7,
        }


class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    level = LevelField(choices=models.Student.Level.choices)
    assessment = AssessmentField(read_only=True)
    task_statuses = StudentTaskStatusSerializer(many=True)
    group = serializers.StringRelatedField()

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
    level = LevelField(choices=models.Group.Level.choices)
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
    level = LevelField(choices=models.ClassYear.Level.choices)
    missions = MissionField(many=True, read_only=True)
    tasks = ClassYearTaskSerializer(many=True, read_only=True)

    class Meta:
        model = models.ClassYear
        fields = ['name', 'health', 'exp', 'level', 'vision', 'missions', 'tasks']
