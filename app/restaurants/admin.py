from django.contrib import admin
from app.restaurants.models import Table, Reservation


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "seats")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("start", "end", "table")