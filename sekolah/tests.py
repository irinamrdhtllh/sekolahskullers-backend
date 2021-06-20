from django.test import TestCase

from .models import Student


class StudentModelTests(TestCase):
    def test_max_level(self):
        student = Student(level='LV3', exp=2500)
        student.update_level()

        self.assertIs(student.level, 'LV3')

    def test_relative_exp(self):
        student = Student(exp=1500)
        student.update_level()

        self.assertAlmostEqual(student.relative_exp(), 50.0)
