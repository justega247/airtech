import json
from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseViewTest(APITestCase):
    client = APIClient()


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
