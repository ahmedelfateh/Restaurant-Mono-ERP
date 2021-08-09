from django.urls import path

from app.restaurants.views import (
    CreateTableView,
    ListTableAPIView,
    DeleteTableAPIView,
    CreateReservationView,
    ListReservationAdminAPIView,
    ListTodayReservationAPIView,
    DeleteReservationAPIView,
    GetAvilableReservationSlotsAPIView,
)


app_name = "restaurants"

urlpatterns = [
    # Tables
    path("tables/create/", CreateTableView.as_view()),
    path("tables/", ListTableAPIView.as_view()),
    path("tables/<int:id>/delete/", DeleteTableAPIView.as_view()),
    # Reservations
    path("reservations/table/<int:table_id>/create/", CreateReservationView.as_view()),
    path("reservations/today/", ListTodayReservationAPIView.as_view()),
    path("reservations/", ListReservationAdminAPIView.as_view()),
    path("reservations/<int:id>/delete/", DeleteReservationAPIView.as_view()),
    path("reservations/slots/", GetAvilableReservationSlotsAPIView.as_view()),
]
