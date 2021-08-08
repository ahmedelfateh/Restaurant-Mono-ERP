from datetime import datetime
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
        # data = serializer.data

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
        qs = Reservation.objects.filter(date=str(datetime.now().date()))
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
    queryset = Reservation.objects.filter(date=str(datetime.now().date()))
    lookup_field = "id"

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)