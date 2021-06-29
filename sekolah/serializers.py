from django.contrib.auth.models import User

from rest_framework import serializers

from .models import (
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

    class Meta:
        model = StudentTaskStatus
        fields = ['task', 'is_complete', 'score', 'is_required', 'deadline', 'max_score']


class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    level = serializers.CharField(source='get_level_display')
    group = serializers.StringRelatedField()
    task_statuses = StudentTaskStatusSerializer(many=True)

    class Meta:
        model = Student
        fields = [
            'username',
            'first_name',
            'last_name',
            'health',
            'exp',
            'level',
            'group',
            'task_statuses',
        ]


class GroupTaskStatusSerializer(serializers.ModelSerializer):
    task = serializers.StringRelatedField()

    class Meta:
        model = GroupTaskStatus
        fields = ['task', 'is_complete', 'score']


class GroupSerializer(serializers.ModelSerializer):
    level = serializers.CharField(source='get_level_display')
    task_statuses = GroupTaskStatusSerializer(many=True)
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['name', 'health', 'exp', 'level', 'task_statuses', 'students']


class ClassYearTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassYearTask
        fields = ['name', 'is_complete', 'score']


class ClassYearSerializer(serializers.ModelSerializer):
    level = serializers.CharField(source='get_level_display')
    tasks = ClassYearTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['name', 'health', 'exp', 'level', 'tasks']
