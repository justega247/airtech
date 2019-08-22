from django.urls import path
from .views import (
    RegisterUsersView
)

urlpatterns = [
    path('auth/register/', RegisterUsersView.as_view(), name="auth-register")
]
