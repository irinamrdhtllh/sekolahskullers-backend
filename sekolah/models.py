from django.conf import settings
from django.db import models


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
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)

    levels = [LEVEL1, LEVEL2, LEVEL3]
    milestones = [0, 1000, 2000, 3000]

    def __str__(self):
        return f"{self.user.get_username()} - {self.user.get_full_name()}"

    def update_level(self):
        """
        Menentukan level berdasarkan batas nilai exp. Contoh: Jika exp berada di dalam
        rentang 1000 <= exp < 2000 maka level menjadi Level 2.
        """
        for i in range(len(self.levels)):
            if (
                self.exp >= self.milestones[i]
                and self.exp < self.milestones[i + 1]
            ):
                self.level = self.levels[i]

    def relative_exp(self):
        """
        Menghitung nilai exp relatif (dalam persen) pada level saat ini.
        Contoh: Jika saat ini Level 2 dan exp bernilai 1500 maka nilai exp relatif adalah 50%.
        """
        for i in range(len(self.levels)):
            if self.level == self.levels[i]:
                low = self.milestones[i]
                high = self.milestones[i + 1]
                return 100 * (self.exp - low) / (high - low)

    def is_alive(self):
        """
        Mengecek jika Student masih hidup (memiliki health positif) atau tidak.
        """
        if self.health > 0:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        self.update_level()
        super().save(*args, **kwargs)


class TaskYear(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_required = models.BooleanField()
    deadline = models.DateTimeField()
    max_yield = models.IntegerField('maximum yield')
    year = models.ManyToManyField(Year)

    def __str__(self):
        return self.name


class TaskGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_required = models.BooleanField()
    deadline = models.DateTimeField()
    max_yield = models.IntegerField('maximum yield')
    group = models.ManyToManyField(Group)

    def __str__(self):
        return self.name


class TaskStudent(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_required = models.BooleanField()
    deadline = models.DateTimeField()
    max_yield = models.IntegerField('maximum yield')
    student = models.ManyToManyField(Student)

    def __str__(self):
        return self.name
