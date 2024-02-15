from datetime import datetime

from loan_management.models import LoanData
from customer_management.models import CustomerData


class CheckLoanApproval:
    """
    Class for checking loan approval based on customer credit evaluation.

    Methods:
        __init__(customer_id): Initializes with a customer ID.
        calculate_credit(): Combines factors to calculate credit score.
        loan_approval(): Determines approval status and interest rate.

    Attributes:
        customer_id: Unique customer identifier.
        past_loans: Queryset of past loans.

    Returns:
        dict: Loan approval status, interest rate, and corrected rate.
    """

    def __init__(self, customer_id) -> None:
        self.customer_id = customer_id

    def get_loan_paid_on_time(self):
        """
        Calculates percentage of past loans paid on time.
        """

        total_loans = self.past_loans.count()
        timely_paid = 0
        for loan in self.past_loans:
            if loan.tenure == loan.emi_paid_on_time:
                timely_paid += 1
        timely_paid_perc = (timely_paid / total_loans) * 100
        return (timely_paid_perc * 25) / 100

    def get_no_of_loans(self):
        """
        Calculates percentage of the total number of past loans.
        """

        total_loans = self.past_loans.count()
        total_loans_perc = (total_loans / 10) * 100
        return (total_loans_perc * 25) / 100

    def get_current_year_loans(self):
        """
        Calculates percentage of loans taken in the current year.
        """

        current_yr_loans = self.past_loans.filter(start_date__year=2023)
        if current_yr_loans.count() == 0:
            return (100 * 25) / 100
        elif current_yr_loans.count() == 1:
            return (50 * 25) / 100
        else:
            return 0

    def get_loan_volume(self):
        """
        Calculates percentage of available loan volume for the customer.
        """

        loan_amounts = self.past_loans.values_list("loan_amount", flat=True)
        total_past_loan = 0
        for loan_amount in loan_amounts:
            total_past_loan += loan_amount
        loan_limit = CustomerData.objects.get(
            customer_id=self.customer_id
        ).approved_limit
        eligible_loan = int(loan_limit - total_past_loan)
        if eligible_loan > 0:
            eligible_loan_perc = (eligible_loan / loan_limit) * 100
        else:
            eligible_loan_perc = 0
        return (eligible_loan_perc * 25) / 100

    def get_current_emis_sum(self):
        """
        Calculates the sum of current monthly EMIs for the customer.
        """

        current_emis = self.past_loans.filter(
            end_date__gte=datetime.now().date()
        ).values_list("emi_monthly_repayment", flat=True)
        current_total_emi = 0
        for emi in current_emis:
            current_total_emi += emi
        return current_total_emi

    def check_emi_monthly_salary(self, emis_sum):
        """
        Checks if monthly EMIs are within 50% of monthly salary.

        Args:
            emis_sum: Sum of current monthly EMIs.

        Returns:
            bool: True if EMIs are within 50% of monthly salary, False otherwise.
        """

        monthly_salary = CustomerData.objects.get(
            customer_id=self.customer_id
        ).monthly_salary

        if emis_sum > (monthly_salary * 50) / 100:
            return False
        return True

    def calculate_credit(self):
        """
        Combines factors to calculate an overall credit score.

        Returns:
            int: Calculated credit score.
        """

        loan_timely_paid = self.get_loan_paid_on_time()
        total_loans = self.get_no_of_loans()
        current_yr_loans = self.get_current_year_loans()
        loan_volume = self.get_loan_volume()
        emis_sum = self.get_current_emis_sum()
        check_emis = self.check_emi_monthly_salary(emis_sum=emis_sum)

        if check_emis is False:
            credit_score = 0
        elif loan_volume == 0:
            credit_score = 0
        else:
            credit_score = (
                loan_timely_paid + total_loans + current_yr_loans + loan_volume
            )
        return credit_score

    def loan_approval(self):
        """
        Determines loan approval status and interest rate.

        Returns:
            dict: Dictionary containing loan approval status, interest rate, and corrected interest rate.
        """

        self.past_loans = LoanData.objects.filter(customer_id=self.customer_id)
        if self.past_loans.count() == 0:
            credit_rating = 100
        else:
            credit_rating = self.calculate_credit()

        if credit_rating > 50:
            loan_approved = True
            interest_rate = 8
        elif 50 > credit_rating > 30:
            loan_approved = True
            interest_rate = 12
        elif 30 > credit_rating > 10:
            loan_approved = True
            interest_rate = 16
        elif 10 > credit_rating:
            loan_approved = False
            interest_rate = 0
        corrected_interest_rate = interest_rate
        return {
            "approval": loan_approved,
            "interest_rate": interest_rate,
            "corrected_interest_rate": corrected_interest_rate,
        }
