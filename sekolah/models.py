from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError


class Task(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=50, unique=True)
    is_required = models.BooleanField()
    deadline = models.DateTimeField('deadline date')
    max_score = models.IntegerField(verbose_name='maximum score', default=100)
    link = models.CharField(max_length=100, unique=True, null=True)

    def __str__(self):
        return self.name


class Assessment(models.Model):
    student = models.OneToOneField('Student', on_delete=models.CASCADE, null=True)

    assessment1 = models.IntegerField(verbose_name='kepemimpinan', default=0)
    assessment2 = models.IntegerField(verbose_name='keteknikfisikaan', default=0)
    assessment3 = models.IntegerField(verbose_name='kemahasiswaan', default=0)
    assessment4 = models.IntegerField(verbose_name='solidaritas', default=0)
    assessment5 = models.IntegerField(verbose_name='kolaboratif', default=0)
    assessment6 = models.IntegerField(verbose_name='semangat menjelajah', default=0)
    assessment7 = models.IntegerField(verbose_name='semangat memaknai', default=0)

    def __str__(self):
        return self.student.__str__()


class Student(models.Model):
    class Meta:
        ordering = ['user__username']
        verbose_name = 'peserta'
        verbose_name_plural = 'peserta'

    class Level(models.IntegerChoices):
        LEVEL1 = 1, 'Landlubber'
        LEVEL2 = 2, 'Powderboy'
        LEVEL3 = 3, 'Guncrew'
        LEVEL4 = 4, 'Master Gunner'
        LEVEL5 = 5, 'Quartermaster'
        LEVEL6 = 6, 'Boatswain'
        LEVEL7 = 7, 'First Mate'
        LEVEL8 = 8, 'Captain'

    MILESTONES = [0, 700, 1600, 2500, 3600, 4700, 5800, 6900]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    health = models.IntegerField(default=100)
    exp = models.IntegerField(verbose_name='experience', default=0)
    weekly_exp = models.IntegerField(verbose_name='weekly experience', default=0)
    level = models.IntegerField(choices=Level.choices, default=Level.LEVEL1)
    gold = models.IntegerField(default=0)
    potion = models.IntegerField(default=0)
    has_mystery_box = models.BooleanField(default=False)
    group = models.ForeignKey(
        'Group',
        related_name='students',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.user.get_username()} - {self.user.get_full_name()}'

    def update_level(self, level=None):
        """
        Menentukan level berdasarkan batas nilai exp. Contoh: Jika exp berada di dalam
        rentang 1000 <= exp < 2000 maka level menjadi Level 2.
        """
        if self.level == self.Level.values[-1]:
            return

        if level:
            self.level = level
            self.exp = self.MILESTONES[level - 1]
            return

        for i in range(len(self.Level.values)):
            if self.exp >= self.MILESTONES[i] and self.exp < self.MILESTONES[i + 1]:
                self.level = self.Level.values[i]

    def relative_exp(self):
        """
        Menghitung nilai exp relatif (dalam persen) pada level saat ini.
        Contoh: Jika saat ini Level 2 dan exp bernilai 1500 maka nilai exp relatif adalah 50%.
        """
        for i in range(len(self.Level.values)):
            if self.level == self.Level.values[i]:
                low = self.MILESTONES[i]
                high = self.MILESTONES[i + 1]
                return round(100 * (self.exp - low) / (high - low), 3)

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

    def complete_task(self, name, score):
        """
        Menyelesaikan Task bernama name dan memberi skor sebesar score.
        """
        task = self.tasks.get(name=name)
        status = StudentTaskStatus.objects.get(student=self, task=task)
        status.is_complete = True
        status.score = score
        status.save(commit=False)
        self.exp += int(score)
        self.weekly_exp += int(score)
        self.save()


class StudentTask(Task):
    class Meta:
        verbose_name = 'tugas peserta'
        verbose_name_plural = 'tugas peserta'

    students = models.ManyToManyField(
        Student, related_name='tasks', through='StudentTaskStatus'
    )

    def assign(self, student):
        """
        Menambahkan Student ke Task yang diberikan.
        """
        self.save(commit=False)
        self.students.add(student)
        StudentTaskStatus.objects.get_or_create(student=student, task=self)

    def save(self, commit=True, *args, **kwargs):
        super().save(*args, **kwargs)

        # Auto assign all students
        if commit:
            students = Student.objects.all()
            for student in students:
                if not self.students.filter(user__username=student.user.get_username()):
                    self.assign(student)


class StudentTaskStatus(models.Model):
    class Meta:
        verbose_name = 'status tugas peserta'
        verbose_name_plural = 'status tugas peserta'

    student = models.ForeignKey(
        Student, related_name='task_statuses', on_delete=models.CASCADE
    )
    task = models.ForeignKey(
        StudentTask, related_name='statuses', on_delete=models.CASCADE
    )
    is_complete = models.BooleanField(default=False)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.student.user.get_username()} - {self.task.name}'

    def save(self, commit=True, *args, **kwargs):
        if commit and self.is_complete:
            self.student.complete_task(self.task.name, self.score)
        super().save(*args, **kwargs)


class Group(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = 'kelas'
        verbose_name_plural = 'kelas'

    class Level(models.IntegerChoices):
        LEVEL1 = 1, 'Galley'
        LEVEL2 = 2, 'Sloop'
        LEVEL3 = 3, 'Brigantine'
        LEVEL4 = 4, 'Galleon'
        LEVEL5 = 5, "Man o' War"

    MILESTONES = [0, 150, 500, 1000, 1500, 2000]

    name = models.CharField(max_length=25)
    health = models.IntegerField(default=100)
    exp = models.IntegerField(verbose_name='experience', default=0)
    weekly_exp = models.IntegerField(verbose_name='weekly experience', default=0)
    level = models.IntegerField(choices=Level.choices, default=Level.LEVEL1)

    def __str__(self):
        return self.name

    def update_level(self, level=None):
        if self.level == self.Level.values[-1]:
            return

        if level:
            self.level = level
            self.exp = self.MILESTONES[level - 1]
            return

        for i in range(len(self.Level.values)):
            if self.exp >= self.MILESTONES[i] and self.exp < self.MILESTONES[i + 1]:
                self.level = self.Level.values[i]

    def relative_exp(self):
        for i in range(len(self.Level.values)):
            if self.level == self.Level.values[i]:
                low = self.MILESTONES[i]
                high = self.MILESTONES[i + 1]
                return round(100 * (self.exp - low) / (high - low), 3)

    def is_alive(self):
        if self.health > 0:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        self.update_level()
        super().save(*args, **kwargs)

    def complete_task(self, name, score):
        """
        Menyelesaikan Task bernama name dan memberi skor sebesar score.
        """
        task = self.tasks.get(name=name)
        status = GroupTaskStatus.objects.get(group=self, task=task)
        status.is_complete = True
        status.score = score
        status.save(commit=False)
        self.exp += int(score)
        self.weekly_exp += int(score)
        self.save()


class GroupTask(Task):
    class Meta:
        verbose_name = 'tugas kelas'
        verbose_name_plural = 'tugas kelas'

    groups = models.ManyToManyField(
        Group, related_name='tasks', through='GroupTaskStatus'
    )

    def assign(self, group):
        """
        Menambahkan Group ke Task yang diberikan.
        """
        self.save(commit=False)
        self.groups.add(group)
        GroupTaskStatus.objects.get_or_create(group=group, task=self)

    def save(self, commit=True, *args, **kwargs):
        super().save(*args, **kwargs)

        # Auto assign all groups
        if commit:
            groups = Group.objects.all()
            for group in groups:
                if not self.groups.filter(name=group.name):
                    self.assign(group)


class GroupTaskStatus(models.Model):
    class Meta:
        verbose_name = 'status tugas kelas'
        verbose_name_plural = 'status tugas kelas'

    group = models.ForeignKey(
        Group, related_name='task_statuses', on_delete=models.CASCADE
    )
    task = models.ForeignKey(
        GroupTask, related_name='statuses', on_delete=models.CASCADE
    )
    is_complete = models.BooleanField(default=False)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.group.name} - {self.task.name}'

    def save(self, commit=True, *args, **kwargs):
        if commit and self.is_complete:
            self.group.complete_task(self.task.name, self.score)
        super().save(*args, **kwargs)


class Mission(models.Model):
    class_year = models.ForeignKey(
        'ClassYear', related_name='missions', on_delete=models.CASCADE
    )
    text = models.TextField(default='')

    def __str__(self):
        return '#' + str(self.pk)


class ClassYear(models.Model):
    class Meta:
        verbose_name = 'angkatan'
        verbose_name_plural = 'angkatan'

    class Level(models.IntegerChoices):
        LEVEL1 = 1, 'Squadron'
        LEVEL2 = 2, 'Flotilla'
        LEVEL3 = 3, 'Fleet'
        LEVEL4 = 4, 'Armada'

    MILESTONES = [0, 1000, 2000, 3000, 4000]

    name = models.CharField(max_length=25)
    health = models.IntegerField(default=100)
    exp = models.IntegerField(verbose_name='experience', default=0)
    level = models.IntegerField(choices=Level.choices, default=Level.LEVEL1)
    vision = models.TextField(default='')

    def __str__(self):
        return self.name

    def update_level(self, level=None):
        if self.level == self.Level.values[-1]:
            return

        if level:
            self.level = level
            self.exp = self.MILESTONES[level - 1]
            return

        for i in range(len(self.Level.values)):
            if self.exp >= self.MILESTONES[i] and self.exp < self.MILESTONES[i + 1]:
                self.level = self.Level.values[i]

    def relative_exp(self):
        for i in range(len(self.Level.values)):
            if self.level == self.Level.values[i]:
                low = self.MILESTONES[i]
                high = self.MILESTONES[i + 1]
                return round(100 * (self.exp - low) / (high - low), 3)

    def is_alive(self):
        if self.health > 0:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        # Allow only one instance of a model
        # https://stackoverflow.com/questions/39412968/allow-only-one-instance-of-a-model-in-django
        if not self.pk and ClassYear.objects.exists():
            raise ValidationError('There can only be one instance of ClassYear')

        self.update_level()
        super().save(*args, **kwargs)

    def complete_task(self, name, score):
        """
        Menyelesaikan Task bernama name dan memberi skor sebesar score.
        """
        task = self.tasks.get(name=name)
        task.is_complete = True
        task.score = score
        task.save(commit=False)
        self.exp += int(score)
        self.save()


class ClassYearTask(Task):
    class Meta:
        verbose_name = 'tugas angkatan'
        verbose_name_plural = 'tugas angkatan'

    class_year = models.ForeignKey(
        ClassYear, related_name='tasks', on_delete=models.CASCADE
    )
    is_complete = models.BooleanField(default=False)
    score = models.IntegerField(default=0)

    def save(self, commit=True, *args, **kwargs):
        if not self.is_complete and self.score != 0:
            raise Exception('Score must be 0 when the Task is still not completed.')
        if commit and self.is_complete:
            self.class_year.complete_task(self.name, self.score)
        super().save(*args, **kwargs)
