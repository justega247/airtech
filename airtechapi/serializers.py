from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Flight, Booking
from .utils.validations import validate_date, validate_arrival_departure

User = get_user_model()


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password'
        )
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class FLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'

    def validate_departure(self, value):
        if validate_date(value):
            raise serializers.ValidationError(
                'The departure date cannot be in the past'
            )
        return value

    def validate_arrival(self, value):
        if validate_date(value):
            raise serializers.ValidationError(
                'The arrival date cannot be in the past'
            )
        return value

    def validate(self, data):
        arrival = data.get('arrival', None)
        departure = data.get('departure', None)
        if validate_arrival_departure(arrival, departure):
            raise serializers.ValidationError({
                'invalid_dates': _('The arrival date cannot be less than the departure date')
            })
        return data


class BookingSerializer(serializers.ModelSerializer):
    flight = serializers.SlugRelatedField(queryset=Flight.objects.all(), slug_field='flight_number')
    passenger = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = Booking
        fields = '__all__'
