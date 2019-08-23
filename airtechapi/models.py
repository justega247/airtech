from django.db import models
from django.contrib.auth import get_user_model

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
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
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
    flight_number = models.CharField(max_length=7)
    airline = models.CharField(max_length=50)
    passengers = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('flight_number',)

    def __str__(self):
        return self.flight_number
