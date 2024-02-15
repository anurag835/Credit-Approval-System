from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .serializers import CustomerRegisterSerializer


class CustomerRegister(generics.ListCreateAPIView):
    """
    API View for customer registration.

    Allows customers to register and calculates an approved credit limit based on their monthly salary.

    Attributes:
        serializer_class (class): The serializer class for customer registration data.

    Methods:
        post(request, *args, **kwargs): Handles POST requests for customer registration.
            Validates input data, calculates the approved credit limit, and creates a new customer record.

    Raises:
        Exception: Any unexpected error during the registration process.

    Returns:
        Response: A response containing the registered customer data or an error message.
    """

    serializer_class = CustomerRegisterSerializer

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests for customer registration.

        Validates input data, calculates the approved credit limit, and creates a new customer record.

        Args:
            request (Request): The incoming HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            Exception: Any unexpected error during the registration process.

        Returns:
            Response: A response containing the registered customer data or an error message.
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            monthly_salary = serializer.validated_data["monthly_salary"]
            serializer.validated_data["approved_limit"] = 36 * monthly_salary

            self.perform_create(serializer)
            response = serializer.data
            del response["first_name"]
            del response["last_name"]

            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_response_data = {"error_message": str(e)}
            return Response(error_response_data, status=status.HTTP_400_BAD_REQUEST)
