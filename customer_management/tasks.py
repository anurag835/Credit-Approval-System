import openpyxl
from celery import shared_task

from customer_management.models import CustomerData


@shared_task
def inject_customer_data(file_path):
    """
    Asynchronous task to inject customer data from an Excel file into the database.

    Args:
        file_path (str): The path to the Excel file containing customer data.

    Raises:
        Exception: Any unexpected error during data insertion.

    Prints:
        str: Print statements indicating the creation of customer data objects.
    """

    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    count = 1
    for row_num in range(2, sheet.max_row + 1):
        try:
            row = [cell.value for cell in sheet[row_num]]
            (
                customer_id,
                first_name,
                last_name,
                age,
                phone_number,
                monthly_salary,
                approved_limit,
            ) = row
            if first_name:
                CustomerData.objects.create(
                    customer_id=customer_id,
                    first_name=first_name,
                    last_name=last_name,
                    age=age,
                    phone_number=phone_number,
                    monthly_salary=monthly_salary,
                    approved_limit=approved_limit,
                )
                print(f"Created customer data object: {count}")
                count += 1
        except Exception as e:
            print("Error while inserting data:", e)


def start_data_import(file_path):
    """
    Initiates the asynchronous task to import customer data from an Excel file.

    Args:
        file_path (str): The path to the Excel file containing customer data.
    """
    inject_customer_data.delay(file_path)
