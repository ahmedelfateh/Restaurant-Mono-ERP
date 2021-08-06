import pytest

from app.users.models import User
from .factories import UserFactory


@pytest.mark.django_db
def test_user_creation():
    """[summary]
    Test user model, object create
    """

    user = UserFactory(email="elfateh@gmail.com")

    assert user.email == "elfateh@gmail.com"


@pytest.mark.django_db
def test_user_get_absolute_url(user: User):
    """[summary]
    test user models return correct get_absolute_url()
    """

    assert user.get_absolute_url() == f"/users/{user.id}/"
