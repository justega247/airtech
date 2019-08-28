import json
import datetime
from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import Flight

User = get_user_model()


class BaseViewTest(APITestCase):
    client = APIClient()

    def setUp(self):
        user = User.objects.create(username='paddy', email='paddy@mail.com')
        user.set_password('fakepassword')
        user.save()

        super_user = User.objects.create_superuser(username='maddy', email='maddy@mail.com', password='thepassword')
        super_user.save()

    def user_token(self, data):
        url = reverse(
            "auth-login"
        )
        data = data
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        token = response.data.get("token", '')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

    def create_flight(self):
        return Flight.objects.create(
            origin="Lagos",
            destination="Enugu",
            departure="2019-08-26",
            arrival="2019-08-27",
            flight_number="BK 6089",
            airline="Emirates",
            price=15000
        )


class AuthUserAPITest(BaseViewTest):
    """
    Test for the auth/register/ endpoint
    """
    def test_register_a_user_with_valid_details_success(self):
        url = reverse(
            "auth-register"
        )
        response = self.client.post(
            url,
            data=json.dumps({
                "username": "maxwell",
                "password": "password",
                "email": "max@mail.com"
            }),
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_register_a_user_with_invalid_data_fails(self):
        url = reverse(
            "auth-register"
        )
        response = self.client.post(
            url,
            data=json.dumps({
                "username": "",
                "password": "",
                "email": "mail.com"
            }),
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['username'][0] == 'This field may not be blank.'
        assert response.data['password'][0] == 'This field may not be blank.'
        assert response.data['email'][0] == 'Enter a valid email address.'

    def test_login_user_with_valid_data(self):
        url = reverse(
            "auth-login"
        )
        data = {
            "username": "paddy",
            "password": "fakepassword"
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['user'] == data['username']

    def test_login_user_with_invalid_data(self):
        url = reverse(
            "auth-login"
        )
        data = {
            "username": "paddington",
            "password": "password"
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == "Invalid Credentials"


class FlightTest(BaseViewTest):
    """
    Test for the flight/ endpoint
    """
    def test_get_flight_list_with_super_user_success(self):
        flight01 = self.create_flight()
        flight01.save()
        self.user_token(
            data={
                "username": "paddy",
                "password": "fakepassword"
            })
        url = reverse(
            "flight-list"
        )
        response = self.client.get(
            url,
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_create_flight_without_auth_token_fails(self):
        url = reverse(
            "flight-list"
        )
        data = {
            "origin": "Lagos",
            "destination": "Enugu",
            "departure": "2019-08-26",
            "arrival": "2019-08-27",
            "flight_number": "BK 6089",
            "airline": "Emirates",
            "price": 15000
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data['detail'] == "Authentication credentials were not provided."

    def test_create_flight_with_superuser_auth_token_success(self):
        self.user_token(
            data={
                "username": "maddy",
                "password": "thepassword"
            })
        url = reverse(
            "flight-list"
        )
        data = {
            "origin": "Lagos",
            "destination": "Enugu",
            "departure": datetime.datetime.today().strftime('%Y-%m-%d'),
            "arrival": (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
            "flight_number": "BK 6089",
            "airline": "Emirates",
            "price": 15000
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['origin'] == "Lagos"
        assert response.data['destination'] == "Enugu"
        assert response.data['id'] == 1

    def test_create_flight_with_invalid_date_fails(self):
        self.user_token(
            data={
                "username": "maddy",
                "password": "thepassword"
            })
        url = reverse(
            "flight-list"
        )
        data = {
            "origin": "Lagos",
            "destination": "Enugu",
            "departure": "2019-08-24",
            "arrival": "2019-08-25",
            "flight_number": "BK 6089",
            "airline": "Emirates",
            "price": 15000
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['departure'][0] == "The departure date cannot be in the past"
        assert response.data['arrival'][0] == "The arrival date cannot be in the past"

    def test_create_flight_with_arrival_date_less_than_departure_date_fails(self):
        self.user_token(
            data={
                "username": "maddy",
                "password": "thepassword"
            })
        url = reverse(
            "flight-list"
        )
        data = {
            "origin": "Lagos",
            "destination": "Enugu",
            "departure": (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
            "arrival": datetime.datetime.today().strftime('%Y-%m-%d'),
            "flight_number": "BK 6089",
            "airline": "Emirates",
            "price": 15000
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['invalid_dates'][0] == "The arrival date cannot be less than the departure date"

    def test_get_flight_detail_with_super_user_success(self):
        flight01 = self.create_flight()
        flight01.save()
        self.user_token(
            data={
                "username": "maddy",
                "password": "thepassword"
            })
        url = reverse(
            "flight-detail",
            kwargs={
                "pk": flight01.id
            }
        )
        response = self.client.get(
            url,
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['origin'] == "Lagos"
        assert response.data['destination'] == "Enugu"

    def test_update_flight_detail_with_super_user_success(self):
        flight01 = self.create_flight()
        flight01.save()
        self.user_token(
            data={
                "username": "maddy",
                "password": "thepassword"
            })
        url = reverse(
            "flight-detail",
            kwargs={
                "pk": flight01.id
            }
        )
        response = self.client.get(
            url,
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['origin'] == "Lagos"
        assert response.data['destination'] == "Enugu"
        data = {
            "origin": "Lagos",
            "destination": "Abuja",
            "departure": datetime.datetime.today().strftime('%Y-%m-%d'),
            "arrival": (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
            "flight_number": "BK 6089",
            "airline": "Emirates",
            "price": 15000,
            "type_of_flight": "RT",
            "flight_status": "C"
        }
        response = self.client.put(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['destination'] == "Abuja"
        response = self.client.get(
            url,
            content_type="application/json"
        )
        assert response.data['destination'] == "Abuja"

    def test_delete_flight_detail_with_super_user_success(self):
        flight01 = self.create_flight()
        flight01.save()
        self.user_token(
            data={
                "username": "maddy",
                "password": "thepassword"
            })
        url = reverse(
            "flight-detail",
            kwargs={
                "pk": flight01.id
            }
        )
        response = self.client.delete(
            url,
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = self.client.get(
            url,
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


class BookingTest(BaseViewTest):
    """
    Test the booking/endpoint
    """
    def test_create_booking_with_valid_details_success(self):
        flight01 = self.create_flight()
        flight01.save()
        self.user_token(
            data={
                "username": "maddy",
                "password": "thepassword"
            })
        url = reverse(
            "booking-list"
        )
        data = {
            "flight": "BK 6089"
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['number_of_tickets'] == 1
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_update_booking_with_details_success(self):
        flight01 = self.create_flight()
        flight01.save()
        self.user_token(
            data={
                "username": "maddy",
                "password": "thepassword"
            })
        url = reverse(
            "booking-list",
        )
        data = {
            "flight": "BK 6089"
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['number_of_tickets'] == 1
        url = reverse(
            "booking-detail",
            kwargs={
                "pk": response.data['id']
            }
        )
        response = self.client.get(
            url,
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['number_of_tickets'] == 1
        url = reverse(
            "booking-detail",
            kwargs={
                "pk": response.data['id']
            }
        )
        data = {
            "flight": "BK 6089",
            "number_of_tickets": 2
        }
        response = self.client.put(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['number_of_tickets'] == 2
        self.client.credentials()
        self.user_token(
            data={
                "username": "paddy",
                "password": "fakepassword"
            })
        data = {
            "flight": "BK 6089",
            "number_of_tickets": 2
        }
        response = self.client.put(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
