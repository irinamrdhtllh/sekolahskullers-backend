from django.conf import settings
from django.db import models


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    health = models.IntegerField(default=100)
    exp = models.IntegerField(default=0)

    LEVEL1 = 'LV1'
    LEVEL2 = 'LV2'
    LEVEL3 = 'LV3'
    LEVEL_CHOICES = [
        (LEVEL1, 'Level 1'),
        (LEVEL2, 'Level 2'),
        (LEVEL3, 'Level 3'),
    ]
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES, default=LEVEL1)
    group = models.ForeignKey(Group)

    def __str__(self):
        return f"{self.user.username} - {self.user.first_name} {self.user.last_name}"


class Group(models.Model):
    name = models.CharField(max_length=25, unique=True)
    health = models.IntegerField(default=100)
    exp = models.IntegerField(default=0)

    LEVEL1 = 'LV1'
    LEVEL2 = 'LV2'
    LEVEL3 = 'LV3'
    LEVEL_CHOICES = [
        (LEVEL1, 'Level 1'),
        (LEVEL2, 'Level 2'),
        (LEVEL3, 'Level 3'),
    ]
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES, default=LEVEL1)

    def __str__(self):
        return self.name


class Year(models.Model):
    name = models.CharField(max_length=25, unique=True)
    health = models.IntegerField(default=100)
    exp = models.IntegerField(default=0)

    LEVEL1 = 'LV1'
    LEVEL2 = 'LV2'
    LEVEL3 = 'LV3'
    LEVEL_CHOICES = [
        (LEVEL1, 'Level 1'),
        (LEVEL2, 'Level 2'),
        (LEVEL3, 'Level 3'),
    ]
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES, default=LEVEL1)

    vision = models.TextField()
    mission = models.TextField()

    def __str__(self):
        return self.name


class TaskStudent(models.Model):
    name = models.CharField(max_length=50, unique=True)
    required = models.BooleanField()
    deadline = models.DateTimeField()
    max_yield = models.IntegerField('maximum yield')
    student = models.ManyToManyField(Student)

    def __str__(self):
        return self.name


class TaskGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)
    required = models.BooleanField()
    deadline = models.DateTimeField()
    max_yield = models.IntegerField('maximum yield')
    group = models.ManyToManyField(Group)

    def __str__(self):
        return self.name


class TaskYear(models.Model):
    name = models.CharField(max_length=50, unique=True)
    required = models.BooleanField()
    deadline = models.DateTimeField()
    max_yield = models.IntegerField('maximum yield')
    year = models.ManyToManyField(Year)

    def __str__(self):
        return self.name
