from rest_framework import serializers
from app.users.models import User


class UserSerializer(serializers.ModelSerializer):

    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ["id", "name", "employee_number", "role"]


class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ["id", "name", "employee_number", "role", "password"]

    def validate_employee_number(self, value):
        qs = User.objects.filter(employee_number__iexact=str(value))
        if qs.exists():
            raise serializers.ValidationError(
                "User with this Employee Number already exists"
            )

        if len(str(value)) > 4 or len(str(value)) < 4:
            raise serializers.ValidationError("Must be 4 degits")
        return value

    def validate_password(self, value):
        if len(str(value)) > 6 or len(str(value)) < 6:
            raise serializers.ValidationError("Passwords must be 6 characters long")
        return value


class LoginSerializer(serializers.Serializer):
    employee_number = serializers.IntegerField()
    password = serializers.CharField()

    def validate_employee_number(self, value):
        qs = User.objects.filter(employee_number__iexact=str(value))
        if not qs.exists():
            raise serializers.ValidationError("This user it not Registered")
        return value

    def validate(self, attrs):
        user = User.objects.get(employee_number=attrs.get("employee_number"))
        if user.check_password(attrs.get("password")) is not True:
            raise serializers.ValidationError("Password is not correct")

        return attrs
