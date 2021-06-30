from django.contrib.auth.models import User

from rest_framework import serializers

from .models import (
    Assessment,
    Student,
    StudentTaskStatus,
    Group,
    GroupTaskStatus,
    ClassYear,
    ClassYearTask,
)


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
            raise serializers.ValidationError('Passwords don\'t match')
        return super().validate(data)

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        Student.objects.create(user=user)
        return user


class StudentTaskStatusSerializer(serializers.ModelSerializer):
    task = serializers.StringRelatedField()
    is_required = serializers.BooleanField(source='task.is_required')
    deadline = serializers.DateTimeField(source='task.deadline')
    max_score = serializers.IntegerField(source='task.max_score')
    link = serializers.CharField(source='task.link')

    class Meta:
        model = StudentTaskStatus
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
            'semangat menjelajah': value.assessment6,
            'semangat memaknai': value.assessment7,
        }


class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    group = serializers.StringRelatedField()
    task_statuses = StudentTaskStatusSerializer(many=True)
    assessment = AssessmentField(read_only=True)

    class Meta:
        model = Student
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
        model = GroupTaskStatus
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
        model = Group
        fields = ['name', 'health', 'exp', 'level', 'task_statuses', 'students']


class ClassYearTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassYearTask
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
        model = ClassYear
        fields = ['name', 'health', 'exp', 'level', 'vision', 'missions', 'tasks']
