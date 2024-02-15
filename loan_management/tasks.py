import openpyxl
from celery import shared_task

from customer_management.models import CustomerData
from loan_management.models import LoanData


@shared_task
def inject_loan_data(file_path):
    """
    Asynchronous task to inject loan data from an Excel file into the database.

    Args:
        file_path (str): The path to the Excel file containing loan data.

    Raises:
        Exception: Any unexpected error during data insertion.

    Prints:
        str: Print statements indicating the creation of loan data objects.
    """
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    count = 1
    for row_num in range(2, sheet.max_row + 1):
        try:
            row = [cell.value for cell in sheet[row_num]]
            customer_id, loan_id, loan_amount, tenure, interest_rate, monthly_repayment, emis_paid_on_time, start_date, end_date = row
            if customer_id:
                customer_ins = CustomerData.objects.get(customer_id=customer_id)
            
                LoanData.objects.create(
                    customer_id=customer_ins,
                    loan_id=int(loan_id),
                    loan_amount=float(loan_amount),
                    tenure=int(tenure),
                    interest_rate=float(interest_rate),
                    emi_monthly_repayment=float(monthly_repayment),
                    emi_paid_on_time=float(emis_paid_on_time),
                    start_date=start_date,
                    end_date=end_date
                )
                print(f"Created loan data object: {count}")
                count += 1
        except Exception as e:
            print("Error while inserting data:", e)


def start_data_import(file_path):
    """
    Initiates the asynchronous task to import loan data from an Excel file.

    Args:
        file_path (str): The path to the Excel file containing loan data.
    """
    inject_loan_data.delay(file_path)