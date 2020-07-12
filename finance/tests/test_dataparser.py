

from finance.finance.billinfo import BillInfo
from finance.finance.loan import Loan, create_loans
from finance.finance.loaninfo import LoanInfo
from finance.finance.money import Money
import finance.finance.dataparser as parser

import pytest
import yaml


@pytest.fixture
def document():
  return """
  loans:
    - name: First Loan
      loan info:
        balance: 10000.00
        interest: 3.45
      bill info:
        day: 7
        amount: 123.45
  """

def test_loan_with_defaults(document):

  loan_info = LoanInfo(10000.00, 3.45)
  bill_info = BillInfo(7, 123.45)
  expected_loan = Loan(loan_info, bill_info)

  data = parser.parse(document)
  loan_data = parser.get_loans_data(data)
  print(f'What: {loan_data}')
  payers_data = parser.get_payers_data(data)
 
  loan_list = create_loans(loan_data)

  assert len(loan_list) == 1
  assert loan_list[0].balance == Money(10000.00)
  assert loan_list[0].interest == 3.45
  assert loan_list[0].bill_day == 7
  assert loan_list[0].min_payment == 123.45