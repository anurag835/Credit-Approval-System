from django.db import models

from customer_management.models import CustomerData


class LoanData(models.Model):
    customer_id = models.ForeignKey(
        CustomerData, on_delete=models.CASCADE, related_name="loans"
    )
    loan_id = models.AutoField(primary_key=True)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    emi_monthly_repayment = models.DecimalField(max_digits=10, decimal_places=2)
    emi_paid_on_time = models.IntegerField()
    start_date = models.DateField(auto_now=True)
    end_date = models.DateField()
