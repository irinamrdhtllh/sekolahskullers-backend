from rest_framework import serializers

from . import models


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
        pairs = {
            'kepemimpinan': value.assessment1,
            'keteknikfisikaan': value.assessment2,
            'kemahasiswaan': value.assessment3,
            'solidaritas': value.assessment4,
            'kolaboratif': value.assessment5,
            'semangat_menjelajah': value.assessment6,
            'semangat_memaknai': value.assessment7,
        }
        return [{'key': key, 'value': val} for key, val in pairs.items()]


class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    relative_exp = serializers.SerializerMethodField()
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
            'relative_exp',
            'weekly_exp',
            'level',
            'assessment',
            'task_statuses',
            'group',
        ]

    def get_relative_exp(self, student):
        return student.relative_exp()


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
    relative_exp = serializers.SerializerMethodField()
    task_statuses = GroupTaskStatusSerializer(many=True)
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = models.Group
        fields = [
            'name',
            'health',
            'exp',
            'relative_exp',
            'weekly_exp',
            'level',
            'task_statuses',
            'students',
        ]

    def get_relative_exp(self, group):
        return group.relative_exp()


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
    relative_exp = serializers.SerializerMethodField()
    missions = MissionField(many=True, read_only=True)
    tasks = ClassYearTaskSerializer(many=True, read_only=True)

    class Meta:
        model = models.ClassYear
        fields = [
            'name',
            'health',
            'exp',
            'relative_exp',
            'level',
            'vision',
            'missions',
            'tasks',
        ]

    def get_relative_exp(self, class_year):
        return class_year.relative_exp()
