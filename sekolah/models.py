from django.contrib.auth.models import User
from django.db import models


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    health = models.IntegerField(default=100)
    exp = models.IntegerField(verbose_name='experience', default=0)

    class Level(models.IntegerChoices):
        LEVEL1 = 1, 'Level 1'
        LEVEL2 = 2, 'Level 2'
        LEVEL3 = 3, 'Level 3'

    MILESTONES = [0, 1000, 2000, 3000]
    level = models.IntegerField(choices=Level.choices, default=Level.LEVEL1)

    def __str__(self):
        return f"{self.user.get_username()} - {self.user.get_full_name()}"

    def update_level(self):
        """
        Menentukan level berdasarkan batas nilai exp. Contoh: Jika exp berada di dalam
        rentang 1000 <= exp < 2000 maka level menjadi Level 2.
        """
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

    def complete_task(self, name, score):
        """
        Menyelesaikan Task bernama name dan memberi skor sebesar score.
        """
        task = self.task_set.get(name=name)
        status = TaskStatus.objects.get(student=self, task=task)
        status.is_complete = True
        status.score = score
        status.save()
        self.exp += int(score)
        self.save()


class Task(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_required = models.BooleanField()
    deadline = models.DateTimeField('deadline date')
    max_score = models.IntegerField(verbose_name='maximum score', default=100)
    students = models.ManyToManyField(Student, through='TaskStatus')

    def __str__(self):
        return self.name

    def assign(self, student):
        """
        Menambahkan Student ke Task yang diberikan.
        """
        self.save()
        self.students.add(student)
        TaskStatus.objects.get_or_create(student=student, task=self)


class TaskStatus(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)
    score = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'task status'
        verbose_name_plural = 'task statuses'
