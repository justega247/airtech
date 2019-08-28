from django.db import models
from django.contrib.auth import get_user_model
from .utils.validations import alphaonly, alphanumeric

User = get_user_model()


# Create your models here.
class Flight(models.Model):
    ONE_WAY = 'OW'
    ROUND_TRIP = 'RT'
    DIRECT_FLIGHT = 'DF'
    DELAYED = 'D'
    CANCELLED = 'C'
    EN_ROUTE = 'E'
    SCHEDULED = 'S'
    LANDED = 'L'
    REDIRECTED = 'R'
    UNKNOWN = 'U'
    FLIGHT_TYPES = (
        (ONE_WAY, 'One-way'),
        (ROUND_TRIP, 'Round-trip'),
        (DIRECT_FLIGHT, 'Direct-flight')
    )
    FLIGHT_STATUS = (
        (DELAYED, 'Delayed'),
        (CANCELLED, 'Cancelled'),
        (EN_ROUTE, 'En-route'),
        (SCHEDULED, 'Scheduled'),
        (LANDED, 'Landed'),
        (REDIRECTED, 'Redirected'),
        (UNKNOWN, 'Unknown')
    )
    origin = models.CharField(max_length=100, validators=[alphaonly])
    destination = models.CharField(max_length=100, validators=[alphaonly])
    departure = models.DateField()
    arrival = models.DateField()
    type_of_flight = models.CharField(
        max_length=2,
        choices=FLIGHT_TYPES,
        default=ONE_WAY
    )
    flight_status = models.CharField(
        max_length=2,
        choices=FLIGHT_STATUS,
        default=SCHEDULED
    )
    flight_number = models.CharField(max_length=7, validators=[alphanumeric], unique=True)
    airline = models.CharField(max_length=50, validators=[alphaonly])
    price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('flight_number',)

    def __str__(self):
        return self.flight_number


class Booking(models.Model):
    flight = models.ForeignKey(Flight, related_name='bookings', on_delete=models.CASCADE)
    passenger = models.ForeignKey(User, related_name='bookings', on_delete=models.CASCADE)
    number_of_tickets = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('flight', 'passenger')
