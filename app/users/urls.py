from django.urls import path

from app.users.views import (
    CreateUserView,
    LoginView,
)


app_name = "users"

urlpatterns = [
    path("create/", CreateUserView.as_view()),
    path("login/", LoginView.as_view()),
]
