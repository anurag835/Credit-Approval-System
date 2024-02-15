The Loan Management System is an API-based application that provides functionalities for customer registration, loan eligibility check, loan creation, and viewing loan details. The system is designed to streamline the loan application process for customers while ensuring accurate eligibility checks and efficient loan management.

Customer Registration API:

Endpoint: /api/customer/register/
Description: This API allows customers to register by providing their personal information, including monthly salary. The system automatically calculates the approved credit limit based on the monthly salary. Any unexpected errors during the registration process are handled gracefully, providing a clear response to the user.
Loan Eligibility Check API:

Endpoint: /api/loan/check-eligibility/
Description: Customers can check their eligibility for a loan using this API. The system verifies the eligibility based on the provided customer data, including the customer ID. The result of the eligibility check is returned in the response, along with any relevant details. The API handles unexpected errors and provides informative error messages.
Loan Creation API:

Endpoint: /api/loan/create/
Description: This API allows customers to apply for a loan. It checks the eligibility of the customer using the Loan Eligibility Check API, processes the loan creation, and returns the result. If the loan is approved, the system creates a new loan record with details such as monthly installment, repayment date, and approval status. In case of rejection, a suitable message is returned.
View Loan Details API:

Endpoint: /api/loan/view/<loan_id>/
Description: Customers can retrieve detailed information about a specific loan using this API. The system fetches and returns the loan details based on the provided loan ID.
View Customer's Loans API:

Endpoint: /api/customer/loans/<customer_id>/
Description: Customers can view the details of loans associated with their account using this API. The system retrieves and returns the loan information for the specified customer ID.
