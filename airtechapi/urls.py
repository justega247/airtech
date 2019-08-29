from django.urls import path
from .views import (
    RegisterUsersView,
    LoginView,
    FlightListView,
    FlightDetailView,
    BookFlightView,
    BookFlightDetailView,
    UploadPassportView
)

urlpatterns = [
    path('auth/register/', RegisterUsersView.as_view(), name="auth-register"),
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('flight/', FlightListView.as_view(), name="flight-list"),
    path('flight/<int:pk>', FlightDetailView.as_view(), name="flight-detail"),
    path('booking/', BookFlightView.as_view(), name="booking-list"),
    path('booking/<int:pk>', BookFlightDetailView.as_view(), name="booking-detail"),
    path('passport/', UploadPassportView.as_view(), name="passport-upload")
]
