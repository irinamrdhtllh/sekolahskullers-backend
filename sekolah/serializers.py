from rest_framework import serializers

from . import models
from .items import POTION, MYSTERY_BOX


class LevelField(serializers.ChoiceField):
    def to_representation(self, value):
        return {'value': value, 'display': self.grouped_choices[value]}


class StudentTaskStatusSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='task.name')
    is_required = serializers.BooleanField(source='task.is_required')
    deadline = serializers.DateTimeField(source='task.deadline')
    max_score = serializers.IntegerField(source='task.max_score')
    link = serializers.CharField(source='task.link')

    class Meta:
        model = models.StudentTaskStatus
        fields = [
            'name',
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
            'gold',
            'potion',
            'assessment',
            'task_statuses',
            'group',
        ]

    def get_relative_exp(self, student):
        return student.relative_exp()


class GroupTaskStatusSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='task.name')
    is_required = serializers.BooleanField(source='task.is_required')
    deadline = serializers.DateTimeField(source='task.deadline')
    max_score = serializers.IntegerField(source='task.max_score')
    link = serializers.CharField(source='task.link')

    class Meta:
        model = models.GroupTaskStatus
        fields = [
            'name',
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


class ShopSerializer(serializers.Serializer):
    potion = serializers.IntegerField(min_value=1, required=False)
    mystery_box_type = serializers.ChoiceField(
        choices=list(MYSTERY_BOX['price'].keys()), required=False
    )

    def update(self, instance, validated_data):
        potion = validated_data.get('potion')
        mystery_box_type = validated_data.get('mystery_box_type')

        # Buy potion
        if potion:

            if instance.gold < POTION['price']:
                raise serializers.ValidationError(
                    {'potion': ['Insufficient gold to buy potion.']}
                )

            instance.gold -= POTION['price']
            instance.potion += potion

        # Buy mystery box
        if mystery_box_type:

            if instance.has_mystery_box:
                raise serializers.ValidationError(
                    {'mystery_box_type': ['Student still has mystery box.']}
                )

            mystery_box_price = MYSTERY_BOX['price'].get(mystery_box_type)
            if instance.gold < mystery_box_price:
                raise serializers.ValidationError(
                    {
                        'mystery_box_type': [
                            'Insufficient gold to buy selected mystery box.'
                        ]
                    }
                )

            instance.gold -= mystery_box_price

            # NOTE: Change has_mystery_box to False through management command
            instance.has_mystery_box = True

        instance.save()
        return instance
