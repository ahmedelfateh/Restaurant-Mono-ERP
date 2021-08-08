from rest_framework import serializers
from app.restaurants.models import Table, Reservation


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ["id", "number", "seats"]


class CreateTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ["id", "number", "seats"]

    def validate_number(self, value):
        qs = Table.objects.filter(number__iexact=str(value))
        if qs:
            raise serializers.ValidationError(
                "There is a Table with the same number, Please change the number"
            )
        return value

    def validate_seats(self, value):
        if value > 12 or value < 1:
            raise serializers.ValidationError("The Seats Must be from 1 to 12 at max")
        return value


class ReservationSerializer(serializers.ModelSerializer):
    table = TableSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = ["id", "start", "end", "date", "table"]