import datetime
from django.core.validators import RegexValidator

alphaonly = RegexValidator(r'^[a-zA-Z]*$', 'Only alphabets are allowed.')
alphanumeric = RegexValidator(r'^[0-9a-zA-Z ]*$', 'Only alphanumeric characters are allowed.')


def validate_date(date_to_validate):
    present_date = datetime.date.today()
    return present_date > date_to_validate


def validate_arrival_departure(arrival_date, departure_date):
    return arrival_date < departure_date
