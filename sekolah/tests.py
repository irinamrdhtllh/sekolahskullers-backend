from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Student, StudentTaskStatus, Task


class StudentModelTests(TestCase):
    def test_max_level(self):
        student = Student(level='LV3', exp=2500)
        student.update_level()

        self.assertIs(student.level, 'LV3')

    def test_relative_exp(self):
        student = Student(exp=1500)
        student.update_level()

        self.assertAlmostEqual(student.relative_exp(), 50.0)

    def test_complete_task(self):
        user = User.objects.create()
        student = Student.objects.create(user=user)

        task = Task.objects.create(
            name='task', is_required=True, deadline=timezone.now()
        )
        StudentTaskStatus.objects.create(student=student, task=task)

        task.students.add(student)
        student.complete_task('task', 90)

        self.assertEqual(student.studenttaskstatus_set.get(task__name='task').score, 90)
        self.assertEqual(student.studenttaskstatus_set.get(task__name='task').is_complete, True)


class TaskModelTests(TestCase):
    def test_assign_task(self):
        user = User.objects.create()
        student = Student.objects.create(user=user)

        task = Task.objects.create(
            name='task', is_required=True, deadline=timezone.now()
        )
        task.assign(student)

        self.assertEqual(student.task_set.get(name='task'), task)
