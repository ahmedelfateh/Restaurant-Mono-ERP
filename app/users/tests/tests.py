from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from app.users.models import User
from app.users.tests.factories import UserFactory


class UserRegisterTest(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory(
            name="Ahmed", employee_number=1234, role="ADMIN", password="123qwe"
        )
        self.url = "/api/users/"
        self.client = APIClient()
        token = self.user.get_token()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token["access"])

    def test_create_user(self):
        data = {
            "name": "Ahmed",
            "employee_number": 1087,
            "role": "ADMIN",
            "password": "123456",
        }
        response = self.client.post(
            self.url + "create/",
            data=data,
        )

        self.assertEqual(len(User.objects.all()), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user(self):
        data = {
            "employee_number": 1234,
            "password": "123qwe",
        }
        response = self.client.post(
            self.url + "login/",
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
