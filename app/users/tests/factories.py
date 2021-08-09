import factory
import factory.fuzzy
import random
from factory import Faker
from factory.django import DjangoModelFactory
from app.users.models import User


def generate_employee_number():
    return random.randint(1111, 9999)


class UserFactory(DjangoModelFactory):
    """[summary]
    Create fake user for test
    """

    name = factory.Sequence(lambda n: "user {0}".format(n))
    employee_number = generate_employee_number()
    role = factory.fuzzy.FuzzyChoice(User.ROLE_CHOICES)
    password = factory.PostGenerationMethodCall("set_password", "password")

    class Meta:
        model = User
        django_get_or_create = ["employee_number"]
