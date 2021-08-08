from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.deletion import PROTECT


def validate_seats_number(value):
    if value > 12 or value < 1:
        raise ValidationError("The Seats Must be from 1 to 12 at max")


class Table(models.Model):
    number = models.IntegerField("Table Number", blank=False, null=False, unique=True)
    seats = models.IntegerField(
        "Seats Number",
        blank=False,
        null=False,
        validators=[validate_seats_number],
    )

    class Meta:
        ordering = ["number"]
        verbose_name = "Table"
        verbose_name_plural = "Tables"

    def __str__(self):
        return f"{self.number}"


class Reservation(models.Model):
    start = models.TimeField(
        "Reservation Start Time", blank=False, null=False, default=None
    )
    end = models.TimeField(
        "Reservation End Time", blank=False, null=False, default=None
    )
    date = models.DateField("Reservation date", blank=False, null=False, default=None)
    table = models.ForeignKey(
        Table, blank=False, null=False, on_delete=PROTECT, related_name="reservation"
    )

    class Meta:
        ordering = ["start"]
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"

    def __str__(self):
        return f"{self.table}"
