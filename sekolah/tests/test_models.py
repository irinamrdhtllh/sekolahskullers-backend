from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from sekolah import models


def create_student(username='user', **kwargs):
    user = User.objects.create(username=username)
    student = models.Student.objects.create(user=user, **kwargs)
    return student


class StudentModelTests(TestCase):
    def test_update_level(self):
        student1 = create_student(username='1', exp=300)
        student2 = create_student(username='2', exp=800)
        student3 = create_student(username='3', exp=1700)

        self.assertIs(student1.level, models.Student.Level.LEVEL1.value)
        self.assertIs(student2.level, models.Student.Level.LEVEL2.value)
        self.assertIs(student3.level, models.Student.Level.LEVEL3.value)

    def test_update_level_assign(self):
        student = create_student()

        student.update_level(4)

        self.assertIs(student.level, models.Student.Level.LEVEL4.value)

    def test_max_level(self):
        student = create_student(level=8)

        student.update_level()

        self.assertIs(student.level, models.Student.Level.LEVEL8.value)

    def test_relative_exp(self):
        student = create_student(exp=3050)

        self.assertAlmostEqual(student.relative_exp(), 50.0)

    def test_complete_task(self):
        student = create_student()

        task = models.StudentTask.objects.create(
            name='task', is_required=True, deadline=timezone.now()
        )
        models.StudentTaskStatus.objects.create(student=student, task=task)

        task.students.add(student)
        student.complete_task('task', 90)

        self.assertEqual(student.task_statuses.get(task__name='task').score, 90)
        self.assertEqual(student.task_statuses.get(task__name='task').is_complete, True)


class StudentTaskModelTests(TestCase):
    def test_assign_task(self):
        student = create_student()

        task = models.StudentTask.objects.create(
            name='task', is_required=True, deadline=timezone.now()
        )
        task.assign(student)

        self.assertEqual(student.tasks.get(name='task'), task)


class GroupModelTests(TestCase):
    def test_update_level(self):
        group1 = models.Group.objects.create(name='1', exp=100)
        group2 = models.Group.objects.create(name='2', exp=200)
        group3 = models.Group.objects.create(name='3', exp=700)

        self.assertIs(group1.level, models.Group.Level.LEVEL1.value)
        self.assertIs(group2.level, models.Group.Level.LEVEL2.value)
        self.assertIs(group3.level, models.Group.Level.LEVEL3.value)

    def test_update_level_assign(self):
        group = models.Group.objects.create()

        group.update_level(4)

        self.assertIs(group.level, models.Group.Level.LEVEL4.value)

    def test_max_level(self):
        group = models.Group.objects.create(level=5)

        group.update_level()

        self.assertIs(group.level, models.Group.Level.LEVEL5.value)

    def test_relative_exp(self):
        group = models.Group.objects.create(exp=750)

        self.assertAlmostEqual(group.relative_exp(), 50.0)

    def test_complete_task(self):
        group = models.Group.objects.create()

        task = models.GroupTask.objects.create(
            name='task', is_required=True, deadline=timezone.now()
        )
        models.GroupTaskStatus.objects.create(group=group, task=task)

        task.groups.add(group)
        group.complete_task('task', 90)

        self.assertEqual(group.task_statuses.get(task__name='task').score, 90)
        self.assertEqual(group.task_statuses.get(task__name='task').is_complete, True)


class GroupTaskModelTests(TestCase):
    def test_assign_task(self):
        group = models.Group.objects.create()

        task = models.GroupTask.objects.create(
            name='task', is_required=True, deadline=timezone.now()
        )
        task.assign(group)

        self.assertEqual(group.tasks.get(name='task'), task)


class ClassYearModelTests(TestCase):
    def test_update_level(self):
        class_year1 = models.ClassYear.objects.create(name='1', exp=500)
        class_year2 = models.ClassYear.objects.create(name='2', exp=1500)
        class_year3 = models.ClassYear.objects.create(name='3', exp=2500)

        self.assertIs(class_year1.level, models.ClassYear.Level.LEVEL1.value)
        self.assertIs(class_year2.level, models.ClassYear.Level.LEVEL2.value)
        self.assertIs(class_year3.level, models.ClassYear.Level.LEVEL3.value)

    def test_update_level_assign(self):
        class_year = models.ClassYear.objects.create()

        class_year.update_level(2)

        self.assertIs(class_year.level, models.ClassYear.Level.LEVEL2.value)

    def test_max_level(self):
        class_year = models.ClassYear.objects.create(level=4)

        class_year.update_level()

        self.assertIs(class_year.level, models.ClassYear.Level.LEVEL4.value)

    def test_relative_exp(self):
        class_year = models.ClassYear.objects.create(exp=2500)

        self.assertAlmostEqual(class_year.relative_exp(), 50.0)

    def test_complete_task(self):
        class_year = models.ClassYear.objects.create()

        models.ClassYearTask.objects.create(
            name='task',
            is_required=True,
            deadline=timezone.now(),
            class_year=class_year,
        )

        class_year.complete_task('task', 90)

        self.assertEqual(class_year.tasks.get(name='task').score, 90)
        self.assertEqual(class_year.tasks.get(name='task').is_complete, True)
