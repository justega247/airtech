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
            'id',
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


class BookingSerializer(serializers.ModelSerializer):
    flight = serializers.SlugRelatedField(queryset=Flight.objects.all(), slug_field='flight_number')
    passenger = UserDataSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'


class FLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            'id',
            'origin',
            'destination',
            'arrival',
            'departure',
            'type_of_flight',
            'flight_status',
            'flight_number',
            'airline',
            'price',
        )

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


class FlightDetailSerializer(FLightSerializer):
    bookings = BookingSerializer(many=True, read_only=True)
    type_of_flight = serializers.ChoiceField(
            choices=Flight.FLIGHT_TYPES
        )
    type_of_flight_detail = serializers.CharField(
        source='get_type_of_flight_display',
        read_only=True
    )

    flight_status = serializers.ChoiceField(
        choices=Flight.FLIGHT_STATUS
    )
    flight_status_detail = serializers.CharField(
        source='get_flight_status_display',
        read_only=True
    )

    class Meta(FLightSerializer.Meta):
        fields = FLightSerializer.Meta.fields + (
            'type_of_flight_detail',
            'flight_status_detail',
            'created_at',
            'modified_at',
            'bookings'
        )
