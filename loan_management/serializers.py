from rest_framework import serializers

from customer_management.models import CustomerData
from .models import LoanData


class CreateLoanSerializer(serializers.ModelSerializer):

    loan_id = serializers.ReadOnlyField()
    emi_monthly_repayment = serializers.ReadOnlyField()

    class Meta:
        model = LoanData
        fields = (
            "loan_id",
            "customer_id",
            "loan_amount",
            "interest_rate",
            "tenure",
            "emi_monthly_repayment",
        )


class ViewLoanSerializer(serializers.ModelSerializer):

    customer = serializers.SerializerMethodField()

    class Meta:
        model = LoanData
        fields = (
            "loan_id",
            "customer",
            "loan_amount",
            "interest_rate",
            "emi_monthly_repayment",
            "tenure",
        )

    def get_customer(self, obj):
        return CustomerData.objects.filter(
            customer_id=obj.customer_id.customer_id
        ).values(
            "customer_id",
            "first_name",
            "last_name",
            "phone_number",
            "age",
        )


class ViewCustomerLoanSerializer(serializers.ModelSerializer):

    repayments_left = serializers.SerializerMethodField()

    class Meta:
        model = LoanData
        fields = (
            "loan_id",
            "loan_amount",
            "interest_rate",
            "emi_monthly_repayment",
            "repayments_left",
        )

    def get_repayments_left(self, obj):
        return int(obj.tenure - obj.emi_paid_on_time)
