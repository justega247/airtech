from django.urls import path
from .views import (
    RegisterUsersView,
    LoginView
)

urlpatterns = [
    path('auth/register/', RegisterUsersView.as_view(), name="auth-register"),
    path('auth/login/', LoginView.as_view(), name="auth-login")
]
