from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken


def validate_employee_number(value):
    if len(str(value)) > 4 or len(str(value)) < 4:
        raise ValidationError("Must be 4 degits")


class UserManager(BaseUserManager):
    # pylint: disable=arguments-differ
    def _create_user(self, username, employee_number, password, **extra_fields):
        """[summary]
        Create and save a user with the given username, email, and password.
        """

        user = self.model(employee_number=employee_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, employee_number, password, **extra_fields):
        return super().create_user("", employee_number, password, **extra_fields)

    def create_superuser(self, employee_number, password, **extra_fields):
        user = super().create_superuser("", employee_number, password, **extra_fields)
        user.role = "ADMIN"
        user.save(using=self._db)


class User(AbstractUser):
    """[summary]
    User Model

    Extended from the AbstractUser of Django
    """

    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("EMPLOYEE", "Employee"),
    )

    username = None  # type: ignore
    name = models.CharField("Name", blank=False, null=False, max_length=10)
    employee_number = models.IntegerField(
        "Employee Number",
        blank=False,
        null=False,
        unique=True,
        validators=[validate_employee_number],
    )
    role = models.CharField(
        "Role", null=False, blank=False, max_length=10, choices=ROLE_CHOICES
    )

    objects = UserManager()

    USERNAME_FIELD = "employee_number"
    REQUIRED_FIELDS = []  # type: ignore

    class Meta:
        ordering = ["employee_number"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.employee_number}"

    def get_token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
        }

    def is_admin(self):
        return self.role == "ADMIN"
