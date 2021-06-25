from rest_framework import serializers

from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    level = serializers.CharField(source='get_level_display')

    class Meta:
        model = Student
        fields = ['username', 'first_name', 'last_name', 'health', 'exp', 'level']
