from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Student, TaskStatus, Task


def create_student(username='user', **kwargs):
    user = User.objects.create(username=username)
    student = Student.objects.create(user=user, **kwargs)
    return student


class StudentModelTests(TestCase):
    def test_update_level(self):
        student1 = create_student(username='1', exp=500)
        student2 = create_student(username='2', exp=1200)
        student3 = create_student(username='3', exp=2300)

        self.assertIs(student1.level, Student.Level.LEVEL1.value)
        self.assertIs(student2.level, Student.Level.LEVEL2.value)
        self.assertIs(student3.level, Student.Level.LEVEL3.value)

    def test_relative_exp(self):
        student = create_student(exp=1500)

        self.assertAlmostEqual(student.relative_exp(), 50.0)

    def test_complete_task(self):
        student = create_student()

        task = Task.objects.create(
            name='task', is_required=True, deadline=timezone.now()
        )
        TaskStatus.objects.create(student=student, task=task)

        task.students.add(student)
        student.complete_task('task', 90)

        self.assertEqual(student.taskstatus_set.get(task__name='task').score, 90)
        self.assertEqual(
            student.taskstatus_set.get(task__name='task').is_complete, True
        )


class TaskModelTests(TestCase):
    def test_assign_task(self):
        student = create_student()

        task = Task.objects.create(
            name='task', is_required=True, deadline=timezone.now()
        )
        task.assign(student)

        self.assertEqual(student.task_set.get(name='task'), task)
