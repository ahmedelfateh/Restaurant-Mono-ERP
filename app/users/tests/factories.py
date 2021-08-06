import factory
from factory import Faker
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save


@factory.django.mute_signals(post_save)
class UserFactory(DjangoModelFactory):
    """[summary]
    Create fake user for test
    """

    email = Faker("email")
    password = Faker("password")

    class Meta:
        model = get_user_model()
        django_get_or_create = ["email"]
