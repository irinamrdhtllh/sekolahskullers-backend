from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase

from sekolah import models

from .test_models import create_student


class PublicAPITests(APITestCase):
    def setUp(self):
        self.STUDENT_COUNT = 82
        self.GROUP_COUNT = 10

        for i in range(self.STUDENT_COUNT):
            create_student(f'Student {i}')

        for i in range(self.GROUP_COUNT):
            models.Group.objects.create(name=f'Group {i}')

        models.ClassYear.objects.create(name='My Class Year')

    def test_students(self):
        response = self.client.get('/api/students/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Student.objects.count(), self.STUDENT_COUNT)

    def test_groups(self):
        response = self.client.get('/api/groups/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Group.objects.count(), self.GROUP_COUNT)

    def test_class_year(self):
        response = self.client.get('/api/class-year/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.ClassYear.objects.count(), 1)


class PrivateAPITests(APITestCase):
    def setUp(self):
        self.group = models.Group.objects.create(name='My Group')
        self.student = create_student(username='Me', group=self.group)

        refresh = RefreshToken.for_user(self.student.user)
        self.access_token = str(refresh.access_token)

    def test_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = self.client.get('/api/profile/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], self.student.user.get_username())

    def test_profile_group(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = self.client.get('/api/profile/group/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.group.name)
