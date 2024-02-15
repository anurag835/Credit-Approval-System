from datetime import date

from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import LoanData

from customer_management.models import CustomerData


class CheckEligibilityAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.customer_data = CustomerData.objects.create(
            customer_id=16,
            first_name="John",
            last_name="Doe",
            age=30,
            phone_number=1234567890,
            monthly_salary=50000,
            approved_limit=50000 * 36,
        )

    def test_check_eligibility_api(self):
        # Data for API request
        data = {
            "customer_id": 16,
            "loan_amount": 200000,
            "interest_rate": 8,
            "tenure": 14,
        }

        response = self.client.post(reverse("check_eligibility"), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate the response structure
        expected_response_data = {
            "customer_id": 16,
            "interest_rate": 8,
            "tenure": 14,
            "approval": True,
            "corrected_interest_rate": 8,
        }
        self.assertEqual(response.data, expected_response_data)

    def test_eligibility_with_previous_loans(self):
        LoanData.objects.create(
            customer_id=self.customer_data,
            loan_amount=100000,
            interest_rate=8.00,
            tenure=12,
            emi_monthly_repayment=9000.00,
            emi_paid_on_time=3,
            start_date=date(2023, 6, 23),
            end_date=date(2024, 6, 23),
        )

        # same customer with another loan
        LoanData.objects.create(
            customer_id=self.customer_data,
            loan_amount=150000,
            interest_rate=10.00,
            tenure=24,
            emi_monthly_repayment=6875.00,
            emi_paid_on_time=4,
            start_date=date(2022, 10, 11),
            end_date=date(2024, 10, 11),
        )

        data = {
            "customer_id": 16,
            "loan_amount": 200000,
            "interest_rate": 8,
            "tenure": 14,
        }

        response = self.client.post(reverse("check_eligibility"), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate the response structure
        expected_response_data = {
            "customer_id": 16,
            "interest_rate": 8,
            "tenure": 14,
            "approval": True,
            "corrected_interest_rate": 8,
        }
        self.assertEqual(response.data, expected_response_data)


class CreateLoanAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a customer with an approved limit (no previous loans)
        self.customer_data = CustomerData.objects.create(
            customer_id=14,
            first_name="John",
            last_name="Doe",
            age=30,
            phone_number=1234567890,
            monthly_salary=50000,
            approved_limit=50000 * 36,
        )

    def test_create_loan_api(self):
        # Test scenario where the customer applies for a loan
        data = {
            "customer_id": 14,
            "loan_amount": 200000,
            "interest_rate": 8,
            "tenure": 14,
        }

        response = self.client.post(reverse("create_loan"), data, format="json")

        # Add assertions for the scenario
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data["loan_id"])
        self.assertEqual(response.data["customer_id"], 14)
        self.assertEqual(response.data["loan_amount"], "200000.00")
        self.assertEqual(response.data["interest_rate"], "8.00")
        self.assertEqual(response.data["tenure"], 14)
        self.assertAlmostEqual(
            response.data["emi_monthly_repayment"], 15428.57142857143, places=2
        )
        self.assertTrue(response.data["loan_approved"])
        self.assertEqual(
            response.data["message"],
            "Congratulations, your loan is approved. Thank you for using our services.",
        )

        # Check if Loan instance is created in the database
        loan_id = response.data["loan_id"]
        self.assertIsNotNone(LoanData.objects.get(pk=loan_id))


class ViewLoanAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a loan for testing
        self.customer_data = CustomerData.objects.create(
            customer_id=16,
            first_name="John",
            last_name="Doe",
            age=30,
            phone_number=1234567890,
            monthly_salary=50000,
            approved_limit=50000 * 36,
        )

        self.loan_data = LoanData.objects.create(
            loan_id=10004,
            customer_id=self.customer_data,
            loan_amount=200000,
            interest_rate=8,
            tenure=14,
            emi_monthly_repayment=15428.57,
            emi_paid_on_time=4,
            start_date=date(2022, 10, 11),
            end_date=date(2024, 10, 11),
        )

    def test_view_loan_api(self):
        response = self.client.get(reverse("view_loan", kwargs={"loan_id": 10004}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Check details of the loan and associated customer
        loan_data = response.data[0]
        self.assertEqual(loan_data["loan_id"], 10004)
        self.assertEqual(loan_data["loan_amount"], "200000.00")
        self.assertEqual(loan_data["interest_rate"], "8.00")
        self.assertEqual(loan_data["emi_monthly_repayment"], "15428.57")
        self.assertEqual(loan_data["tenure"], 14)

        # Check details of the associated customer
        customer_data = loan_data["customer"][0]
        self.assertEqual(customer_data["customer_id"], 16)
        self.assertEqual(customer_data["first_name"], "John")
        self.assertEqual(customer_data["last_name"], "Doe")
        self.assertEqual(customer_data["phone_number"], 1234567890)
        self.assertEqual(customer_data["age"], 30)


class ViewCustomerLoansAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create customer and loans for testing
        self.customer_data = CustomerData.objects.create(
            customer_id=88,
            first_name="Alejandrina",
            last_name="Crespo",
            phone_number=9751473139,
            age=43,
            monthly_salary=50000,
            approved_limit=50000 * 36,
        )

        self.loan_data1 = LoanData.objects.create(
            loan_id=10004,
            customer_id=self.customer_data,
            loan_amount=200000,
            interest_rate=8,
            tenure=14,
            emi_monthly_repayment=15428.57,
            emi_paid_on_time=4,
            start_date=date(2022, 10, 11),
            end_date=date(2024, 10, 11),
        )

    def test_view_customer_loans_api(self):
        response = self.client.get(reverse("view_loans", kwargs={"customer_id": 88}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Check details of the loan and associated customer
        loan_data = response.data[0]
        self.assertEqual(loan_data["loan_id"], 10004)
        self.assertEqual(loan_data["loan_amount"], "200000.00")
        self.assertEqual(loan_data["interest_rate"], "8.00")
        self.assertEqual(loan_data["emi_monthly_repayment"], "15428.57")
        self.assertEqual(loan_data["repayments_left"], 10)
