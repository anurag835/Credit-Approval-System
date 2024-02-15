from django.contrib import admin

from loan_management.models import LoanData

# Register your models here.


class LoanDataAdmin(admin.ModelAdmin):
    list_display = (
        "customer_id",
        "loan_id",
        "loan_amount",
        "tenure",
        "interest_rate",
        "emi_monthly_repayment",
        "emi_paid_on_time",
        "start_date",
        "end_date"
    )




admin.site.register(LoanData, LoanDataAdmin)