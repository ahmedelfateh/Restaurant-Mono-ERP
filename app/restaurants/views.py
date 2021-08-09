import datetime
from rest_framework import response, status, views, generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from app.utils.rest_perm import AdminAccess

from app.restaurants.models import Table, Reservation
from app.restaurants.serializers import (
    TableSerializer,
    CreateTableSerializer,
    ReservationSerializer,
)


class CreateTableView(views.APIView):
    queryset = Table.objects.all()
    serializer_class = CreateTableSerializer
    permission_classes = [IsAuthenticated, AdminAccess]
    authentication_classes = (JWTAuthentication,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        table = Table.objects.create(
            number=data["number"],
            seats=data["seats"],
        )
        table.save()

        return response.Response(
            {
                "status": "success",
                "message": "Table created successfully",
                "user": TableSerializer(table).data,
            },
            status=status.HTTP_200_OK,
        )


class ListTableAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, AdminAccess]
    authentication_classes = (JWTAuthentication,)
    serializer_class = TableSerializer

    def get_queryset(self):
        return Table.objects.all()


class DeleteTableAPIView(
    generics.RetrieveAPIView,
    mixins.DestroyModelMixin,
):
    permission_classes = [IsAuthenticated, AdminAccess]
    authentication_classes = (JWTAuthentication,)
    serializer_class = TableSerializer
    queryset = Table.objects.all()
    lookup_field = "id"

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.reservation.all():
            return response.Response(
                {"msg": "Cant delete this table, have reservations"},
                status=status.HTTP_403_FORBIDDEN,
            )

        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class CreateReservationView(views.APIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated, AdminAccess]
    authentication_classes = (JWTAuthentication,)

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        reservation = Reservation.objects.create(
            table_id=kwargs["table_id"], **serializer.data
        )
        reservation.save()

        return response.Response(
            {
                "status": "success",
                "message": "Reservation created successfully",
                "user": ReservationSerializer(reservation).data,
            },
            status=status.HTTP_200_OK,
        )


class ListReservationAdminAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, AdminAccess]
    authentication_classes = (JWTAuthentication,)
    serializer_class = ReservationSerializer

    def get_queryset(self):
        get_query_params = self.request.query_params.get
        table = get_query_params("table")
        start_date = get_query_params("start_date")
        print(start_date)
        end_date = get_query_params("end_date")
        print(end_date)
        if table:
            return Reservation.objects.filter(table__number=table)
        if start_date and end_date:
            return Reservation.objects.filter(date__range=[start_date, end_date])
        return Reservation.objects.all()


class ListTodayReservationAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)
    serializer_class = ReservationSerializer

    def get_queryset(self):
        qs = Reservation.objects.filter(date=str(datetime.datetime.now().date()))
        get_query_params = self.request.query_params.get
        order = get_query_params("order")
        print(order)
        if order == "asc":
            return qs.order_by("start")
        if order == "dec":
            return qs.order_by("-start")
        return qs


class DeleteReservationAPIView(
    generics.RetrieveAPIView,
    mixins.DestroyModelMixin,
):
    permission_classes = [IsAuthenticated, AdminAccess]
    authentication_classes = (JWTAuthentication,)
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.filter(date=str(datetime.datetime.now().date()))
    lookup_field = "id"

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


def subtract_two_times(time_str):
    open_time = datetime.time(12, 00, 0)
    time = datetime.datetime.strptime(time_str, "%H:%M:%S").time()
    date = datetime.date(1, 1, 1)
    datetime1 = datetime.datetime.combine(date, open_time)
    datetime2 = datetime.datetime.combine(date, time)
    time_elapsed = datetime2 - datetime1
    return time_elapsed


def calculate_available_slots(reservation_list):
    available_slots = []
    for reservation in reservation_list:
        print(reservation["start"])
        if reservation["start"] is None:
            available_slots.append(
                {
                    "tabel_number": reservation["tabel_number"],
                    "start": "12:00:00",
                    "end": "23:59:00",
                }
            )
        if str(subtract_two_times(reservation["start"])) == "0:00:00":
            available_slots.append(
                {
                    "tabel_number": reservation["tabel_number"],
                    "start": "12:00:00",
                    "end": reservation["end"],
                }
            )

    return available_slots


class GetAvilableReservationSlotsAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    def get(self, request, *args, **kwargs):
        guest = request.data.get("guest")
        date = request.data.get("date")

        tables = Table.objects.filter(seats__in=[guest, guest + 1])

        if not tables:
            return response.Response(
                {"msg": "Sorry you can't reserve due too your guest number"}
            )

        # get the avilable not reserved any time tables
        table_free = []
        for table in tables:
            if not table.reservation.all():
                table_free.append(
                    {
                        "tabel_number": table.number,
                        "start": "12:00:00",
                        "end": "23:59:00",
                    }
                )

        table_id_list = []
        for table in tables:
            table_id_list.append(table.id)

        reservation_qs_list = []
        reservation_list = []
        reservations = None
        for table in table_id_list:
            reservations = Reservation.objects.filter(table=table, date=date)
            reservation_qs_list.append(reservations)

        for reservation_qs in reservation_qs_list:
            for reservation in reservation_qs:
                reservation_list.append(
                    {
                        "tabel_number": str(reservation.table.number),
                        "start": str(reservation.start),
                        "end": str(reservation.end),
                    }
                )

        available_slots = calculate_available_slots(reservation_list)

        return response.Response(
            {
                "available_slots": available_slots + table_free,
            }
        )
