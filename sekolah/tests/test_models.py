from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from sekolah import models


def create_student(username='user', **kwargs):
    user = User.objects.create(username=username)
    student = models.Student.objects.create(user=user, **kwargs)
    return student


class StudentModelTests(TestCase):
    def setUp(self):
        self.student = create_student('Me')

    def test_update_level(self):
        for i, exp in enumerate([300, 800, 1700]):
            self.student.exp = exp
            self.student.save()

            self.assertIs(self.student.level, models.Student.Level.values[i])

    def test_update_level_assign(self):
        self.student.update_level(4)

        self.assertIs(self.student.level, models.Student.Level.LEVEL4.value)

    def test_max_level(self):
        self.student.level = 8
        self.student.save()

        self.student.update_level()

        self.assertIs(self.student.level, models.Student.Level.LEVEL8.value)

    def test_relative_exp(self):
        self.student.exp = 3050
        self.student.save()

        self.assertAlmostEqual(self.student.relative_exp(), 50.0)

    def test_complete_task(self):
        models.StudentTask.objects.create(
            name='task', is_required=True, deadline=timezone.now()
        )

        self.student.complete_task('task', 90)

        self.assertEqual(self.student.task_statuses.get(task__name='task').score, 90)
        self.assertEqual(
            self.student.task_statuses.get(task__name='task').is_complete,
            True,
        )


class GroupModelTests(TestCase):
    def setUp(self):
        self.group = models.Group.objects.create(name='My Group')

    def test_update_level(self):
        for i, exp in enumerate([100, 200, 700]):
            self.group.exp = exp
            self.group.save()

            self.assertIs(self.group.level, models.Group.Level.values[i])

    def test_update_level_assign(self):
        self.group.update_level(4)

        self.assertIs(self.group.level, models.Group.Level.LEVEL4.value)

    def test_max_level(self):
        self.group.level = 5
        self.group.save()

        self.group.update_level()

        self.assertIs(self.group.level, models.Group.Level.LEVEL5.value)

    def test_relative_exp(self):
        self.group.exp = 750
        self.group.save()

        self.assertAlmostEqual(self.group.relative_exp(), 50.0)

    def test_complete_task(self):
        models.GroupTask.objects.create(
            name='task', is_required=True, deadline=timezone.now()
        )

        self.group.complete_task('task', 90)

        self.assertEqual(self.group.task_statuses.get(task__name='task').score, 90)
        self.assertEqual(
            self.group.task_statuses.get(task__name='task').is_complete,
            True,
        )


class ClassYearModelTests(TestCase):
    def setUp(self):
        self.class_year = models.ClassYear.objects.create(name='My Class Year')

    def test_update_level(self):
        for i, exp in enumerate([500, 1500, 2500]):
            self.class_year.exp = exp
            self.class_year.save()

            self.assertIs(self.class_year.level, models.ClassYear.Level.values[i])

    def test_update_level_assign(self):
        self.class_year.update_level(2)

        self.assertIs(self.class_year.level, models.ClassYear.Level.LEVEL2.value)

    def test_max_level(self):
        self.class_year.level = 4
        self.class_year.save()

        self.class_year.update_level()

        self.assertIs(self.class_year.level, models.ClassYear.Level.LEVEL4.value)

    def test_relative_exp(self):
        self.class_year.exp = 2500
        self.class_year.save()

        self.assertAlmostEqual(self.class_year.relative_exp(), 50.0)

    def test_complete_task(self):
        models.ClassYearTask.objects.create(
            name='task',
            is_required=True,
            deadline=timezone.now(),
            class_year=self.class_year,
        )

        self.class_year.complete_task('task', 90)

        self.assertEqual(self.class_year.tasks.get(name='task').score, 90)
        self.assertEqual(self.class_year.tasks.get(name='task').is_complete, True)
