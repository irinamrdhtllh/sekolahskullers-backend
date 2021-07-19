from datetime import date, timedelta

from django.contrib.auth.models import User

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase

from sekolah import models
from sekolah.items import POTION, MYSTERY_BOX

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
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token)
        )

    def get_new_student(self):
        return User.objects.get(username='Me').student

    def test_profile(self):
        response = self.client.get('/api/profile/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], self.student.user.get_username())

    def test_profile_group(self):
        response = self.client.get('/api/profile-group/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.group.name)

    def test_buy_potion_success(self):
        self.student.gold = 100
        self.student.save()

        response = self.client.post('/api/shop/', {'potion': 1}, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.get_new_student().gold,
            self.student.gold - POTION['price'],
        )
        self.assertEqual(self.get_new_student().potion, self.student.potion + 1)

    def test_buy_potion_failed(self):
        response = self.client.post('/api/shop/', {'potion': 1}, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            self.get_new_student().gold,
            self.student.gold,
        )
        self.assertEqual(self.get_new_student().potion, self.student.potion)

    def test_buy_mystery_box_success_first_time(self):
        self.student.gold = 100
        self.student.save()

        response = self.client.post(
            '/api/shop/', {'mystery_box_type': 'md'}, format='json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.get_new_student().gold,
            self.student.gold - MYSTERY_BOX['price'].get('md'),
        )
        self.assertEqual(
            self.get_new_student().last_mystery_box_purchase,
            date.today(),
        )

    def test_buy_mystery_box_success_date(self):
        self.student.gold = 100
        self.student.last_mystery_box_purchase = date.today() - timedelta(days=8)
        self.student.save()

        response = self.client.post(
            '/api/shop/', {'mystery_box_type': 'md'}, format='json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.get_new_student().gold,
            self.student.gold - MYSTERY_BOX['price'].get('md'),
        )
        self.assertEqual(
            self.get_new_student().last_mystery_box_purchase,
            date.today(),
        )

    def test_buy_mystery_box_failed_date(self):
        self.student.gold = 100
        self.student.last_mystery_box_purchase = date.today() - timedelta(days=1)
        self.student.save()

        response = self.client.post(
            '/api/shop/', {'mystery_box_type': 'sm'}, format='json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.get_new_student().gold, self.student.gold)
        self.assertEqual(
            self.get_new_student().last_mystery_box_purchase,
            self.student.last_mystery_box_purchase,
        )

    def test_buy_mystery_box_failed_insufficient_gold(self):
        self.student.last_mystery_box_purchase = date.today() - timedelta(days=8)
        self.student.save()

        response = self.client.post(
            '/api/shop/', {'mystery_box_type': 'sm'}, format='json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.get_new_student().gold, self.student.gold)
        self.assertEqual(
            self.get_new_student().last_mystery_box_purchase,
            self.student.last_mystery_box_purchase,
        )
