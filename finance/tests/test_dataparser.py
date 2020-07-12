

from finance.finance.billinfo import BillInfo
from finance.finance.loan import Loan
from finance.finance.loaninfo import LoanInfo
import finance.finance.dataparser as parser

import pytest
import yaml

# 'etc/finance_example.yaml'


def test_no_loans_raise():
  """Make sure that if loans key is not found an exception is raised"""
  document = """
    date: 07-09-2020
  """

  with pytest.raises(parser.ParserError):
    loan_data = parser.parse(document)


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


def test_dummy(document):

  loan_info = LoanInfo(10000.00, 3.45)
  bill_info = BillInfo(7, 123.45)
  expected_loan = Loan(loan_info, bill_info)

  loan_data = parser.parse(document)
  loans = parser.create_loans(loan_data)
