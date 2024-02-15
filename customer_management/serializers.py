from rest_framework import serializers
from .models import CustomerData


class CustomerRegisterSerializer(serializers.ModelSerializer):

    name = serializers.ReadOnlyField()
    approved_limit = serializers.ReadOnlyField()

    class Meta:
        model = CustomerData
        fields = (
            "customer_id",
            "first_name",
            "last_name",
            "name",
            "age",
            "monthly_salary",
            "approved_limit",
            "phone_number",
        )
