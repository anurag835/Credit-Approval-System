from django.urls import path

from . import views

urlpatterns = [
    path(
        "check-eligibility",
        views.CheckEligibility.as_view(),
        name="check_eligibility",
    ),
    path("create-loan", views.CreateLoan.as_view(), name="create_loan"),
    path("view-loan/<int:loan_id>", views.ViewLoan.as_view(), name="view_loan"),
    path(
        "view-loans/<int:customer_id>",
        views.ViewCustomerLoans.as_view(),
        name="view_loans",
    ),
]
