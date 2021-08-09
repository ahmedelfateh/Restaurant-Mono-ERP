from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from app.users.tests.factories import UserFactory
from app.restaurants.models import Table, Reservation
from app.restaurants.tests.factories import TableFactory, ReservationFactory


class TableTest(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory(
            name="Ahmed", employee_number=1234, role="ADMIN", password="123qwe"
        )
        self.table = TableFactory(number=1, seats=12)
        self.url = "/api/restaurants/tables/"
        self.client = APIClient()
        token = self.user.get_token()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token["access"])

    def test_create_table_success(self):
        data = {"number": 2, "seats": 10}
        response = self.client.post(
            self.url + "create/",
            data=data,
        )
        self.assertEqual(len(Table.objects.all()), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_table_fail_on_number(self):
        data = {"number": 1, "seats": 10}
        response = self.client.post(
            self.url + "create/",
            data=data,
        )
        self.assertEqual(len(Table.objects.all()), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_table_fail_on_seats(self):
        data = {"number": 3, "seats": 13}
        response = self.client.post(
            self.url + "create/",
            data=data,
        )
        self.assertEqual(len(Table.objects.all()), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_tables(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_tables(self):
        table = TableFactory(number=10, seats=12)
        self.assertEqual(Table.objects.get(id=(table.id)).number, 10)
        response = self.client.delete(self.url + str(table.id) + "/delete/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_table_with_Reservation(self):
        table = TableFactory(number=10, seats=12)
        reservation = ReservationFactory(table=table)
        self.assertEqual(Table.objects.get(id=(table.id)).number, 10)
        self.assertEqual(Reservation.objects.get(id=(reservation.id)).table.number, 10)
        response = self.client.delete(self.url + str(table.id) + "/delete/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
