from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from .serializers import UserDataSerializer, FLightSerializer, FlightDetailSerializer, BookingSerializer
from .permissions import AnonymousPermissionOnly, IsAdminOrReadOnly, IsCurrentUserOwnerOrReadOnly
from .models import Flight, Booking


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()


# User Related Views
class RegisterUsersView(generics.CreateAPIView):
    """
    POST auth/register/
    """
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = UserDataSerializer


class LoginView(APIView):
    """
    POST auth/login/
    """
    permission_classes = (AnonymousPermissionOnly,)

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        qs = User.objects.filter(username__exact=username)
        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                payload = jwt_payload_handler(user_obj)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token, user=user_obj, request=request)
                return Response(response)
        return Response({
            "error": "Invalid Credentials"
        }, status=status.HTTP_400_BAD_REQUEST)


# Flight Related Views
class FlightListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    serializer_class = FLightSerializer
    queryset = Flight.objects.all()


class FlightDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    serializer_class = FlightDetailSerializer
    queryset = Flight.objects.all()


class BookFlightView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

    def perform_create(self, serializer):
        try:
            serializer.save(passenger=self.request.user)
        except IntegrityError:
            raise ValidationError({
                'message': 'The flight and the passenger fields should be unique together'
            })


class BookFlightDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsCurrentUserOwnerOrReadOnly)
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

    def perform_update(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
            raise ValidationError({
                'message': 'The flight and the passenger fields should be unique together'
            })
