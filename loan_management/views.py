from datetime import date
from dateutil.relativedelta import relativedelta

from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

from loan_management.models import LoanData
from loan_management.utils import CheckLoanApproval
from .serializers import (
    CreateLoanSerializer,
    ViewCustomerLoanSerializer,
    ViewLoanSerializer,
)


class CheckEligibility(APIView):
    """
    API View for checking loan eligibility.

    Allows checking the eligibility of a customer for a loan and provides the result.

    Methods:
        post(request, *args, **kwargs): Handles POST requests for checking loan eligibility.
            Checks the loan eligibility based on the provided customer data and returns the result.

    Raises:
        Exception: Any unexpected error during the eligibility check process.

    Returns:
        Response: A response containing the loan eligibility result or an error message.
    """

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            check_loan_ins = CheckLoanApproval(data["customer_id"])
            result = check_loan_ins.loan_approval()
            response_data = data
            del response_data["loan_amount"]
            response_data.update(result)

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            error_response_data = {"error_message": str(e)}
            return Response(error_response_data, status=status.HTTP_400_BAD_REQUEST)


class CreateLoan(generics.CreateAPIView):
    """
    API View for creating a new loan.

    Allows customers to apply for a loan, checks eligibility, and creates a new loan record if approved.

    Attributes:
        serializer_class (class): The serializer class for creating a new loan.

    Methods:
        post(request, *args, **kwargs): Handles POST requests for creating a new loan.
            Checks loan eligibility, processes loan creation, and returns the result.

    Raises:
        Exception: Any unexpected error during the loan creation process.

    Returns:
        Response: A response containing the loan creation result or an error message.
    """

    serializer_class = CreateLoanSerializer

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            check_loan_ins = CheckLoanApproval(data["customer_id"])
            result = check_loan_ins.loan_approval()
            result["customer_id"] = data["customer_id"]

            if not result["approval"]:
                response_data = {
                    "loan_id": None,
                    "customer_id": result["customer_id"],
                    "loan_approved": result["approval"],
                    "message": "Dear customer, Unfortunately we couldn't approve the loan of your current demand.",
                    "monthly_installement": 0.0,
                }
                return Response(response_data, status=status.HTTP_200_OK)

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)

            loan_amount = data["loan_amount"]
            tenure = data["tenure"]
            monthly_emi = (
                (loan_amount * data["interest_rate"] / 100) + loan_amount
            ) / tenure
            serializer.validated_data["emi_monthly_repayment"] = monthly_emi
            serializer.validated_data["emi_paid_on_time"] = 0
            serializer.validated_data["end_date"] = date.today() + relativedelta(
                months=tenure
            )

            self.perform_create(serializer)
            response = serializer.data
            response["loan_approved"] = result["approval"]
            response["message"] = (
                "Congratulations, your loan is approved. Thank you for using our services."
            )

            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_response_data = {"error_message": str(e)}
            return Response(error_response_data, status=status.HTTP_400_BAD_REQUEST)


class ViewLoan(generics.ListAPIView):
    """
    API View for viewing loan details.

    Allows retrieving details of a specific loan.

    Attributes:
        serializer_class (class): The serializer class for viewing loan details.

    Methods:
        get_queryset(): Returns the queryset of loan data for the specified loan ID.
    """

    serializer_class = ViewLoanSerializer

    def get_queryset(self):
        queryset = LoanData.objects.filter(loan_id=self.kwargs.get("loan_id"))
        return queryset


class ViewCustomerLoans(generics.ListAPIView):
    """
    API View for viewing customer's loans.

    Allows retrieving details of loans associated with a specific customer.

    Attributes:
        serializer_class (class): The serializer class for viewing customer's loan details.

    Methods:
        get_queryset(): Returns the queryset of loan data for the specified customer ID.
    """

    serializer_class = ViewCustomerLoanSerializer

    def get_queryset(self):
        queryset = LoanData.objects.filter(customer_id=self.kwargs.get("customer_id"))
        return queryset
