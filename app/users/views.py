from rest_framework import response, status, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from app.utils.rest_perm import AdminAccess
from app.users.models import User
from app.users.serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
)


class CreateUserView(views.APIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated, AdminAccess]
    authentication_classes = (JWTAuthentication,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        user = User.objects.create(
            name=data["name"],
            employee_number=data["employee_number"],
            role=data["role"],
        )
        user.set_password(data["password"])
        user.save()

        return response.Response(
            {
                "status": "success",
                "message": "User created successfully, You can now use the phone number to login.",
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class LoginView(views.APIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        employee_number = data.get("employee_number")
        user = User.objects.get(employee_number=employee_number)

        return response.Response(
            {
                "status": "success",
                "access_token": user.get_token(),
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )
