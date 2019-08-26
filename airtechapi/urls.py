from django.urls import path
from .views import (
    RegisterUsersView,
    LoginView,
    FlightListView
)

urlpatterns = [
    path('auth/register/', RegisterUsersView.as_view(), name="auth-register"),
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('flight/', FlightListView.as_view(), name="flight-list"),
]
