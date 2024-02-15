from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from customer_management.models import CustomerData


class CustomerRegisterAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_customer_registration(self):
        input_data = {
            "first_name": "abcd",
            "last_name": "defg",
            "age": 24,
            "phone_number": 1234567890,
            "monthly_salary": 38000,
        }

        response = self.client.post(
            reverse("customer_register"), input_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        customer_data = CustomerData.objects.latest("customer_id")
        self.assertEqual(customer_data.monthly_salary, 38000)
        self.assertEqual(customer_data.approved_limit, 36 * 38000)
        self.assertEqual(CustomerData.objects.count(), 1)

        # Validate the response structure
        expected_response_data = {
            "customer_id": customer_data.customer_id,
            "name": "abcd defg",
            "age": 24,
            "monthly_salary": 38000,
            "approved_limit": 1368000,
            "phone_number": 1234567890,
        }
        self.assertEqual(response.data, expected_response_data)
