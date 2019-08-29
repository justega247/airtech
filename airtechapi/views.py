import cloudinary.uploader
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, JSONParser
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from .serializers import (
    UserDataSerializer, FLightSerializer, FlightDetailSerializer, BookingSerializer, ProfileSerializer)
from .permissions import AnonymousPermissionOnly, IsAdminOrReadOnly, IsCurrentUserOwnerOrReadOnly
from .models import Flight, Booking, Profile


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


class UploadPassportView(APIView):
    permission_classes = (IsAuthenticated, IsCurrentUserOwnerOrReadOnly)
    parser_classes = (
        MultiPartParser,
        JSONParser
    )

    def post(self, request):
        passport = request.data.get('passport')

        upload_passport = cloudinary.uploader.upload(
            passport,
            eager=[
                {"width": 1350, "height": 1200}
            ]
        )
        data = {
            "user": self.request.user.pk,
            "passport_url": upload_passport['secure_url'],
            "cloudinary_public_id": upload_passport['public_id']
        }
        serializer = ProfileSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        passport_id = request.data.get('id')
        passport_to_update = get_object_or_404(Profile, id=passport_id)

        passport = request.data.get('passport')

        upload_passport = cloudinary.uploader.upload(
            passport,
            public_id=passport_to_update.cloudinary_public_id,
            eager=[
                {"width": 1350, "height": 1200}
            ]
        )
        data = {
            "user": self.request.user.pk,
            "passport_url": upload_passport['secure_url'],
            "cloudinary_public_id": upload_passport['public_id']
        }
        serializer = ProfileSerializer(passport_to_update, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "data": serializer.data
        }, status=status.HTTP_200_OK)
