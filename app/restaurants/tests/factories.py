import factory
import factory.fuzzy
import datetime
import random
from factory import Faker
from django.utils import timezone
from factory.django import DjangoModelFactory
from app.restaurants.models import Table, Reservation


class TableFactory(DjangoModelFactory):
    """[summary]
    Create fake table for test
    """

    number = 1
    seats = 12

    class Meta:
        model = Table
        django_get_or_create = ["number"]


class ReservationFactory(DjangoModelFactory):
    """[summary]
    Create fake reservation for test
    """

    start = datetime.time(12, 00, 00)
    end = (
        datetime.datetime(2012, 9, 17, 12, 00, 00, 00) + datetime.timedelta(hours=1)
    ).time()
    date = timezone.now()
    table = factory.SubFactory(TableFactory)

    class Meta:
        model = Reservation
        django_get_or_create = ["start"]