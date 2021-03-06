

import datetime

import pytest

from finance.finance.billinfo import BillInfo
from finance.finance.datesubject import DateSubject
from finance.finance.interestaccruer import InterestAccruer
from finance.finance.loan import Loan
from finance.finance.loaninfo import LoanInfo
from finance.finance.money import Money, almost_equal


@pytest.fixture
def current_date():
  """Create date subject for loan to watch."""
  date = datetime.date(2020, 7, 4)
  return DateSubject(date)


def create_loan(accrue_start_date=None):
  # create loan where minimum payment is the day after ptest fixture's date.
  bill_info = BillInfo(day=20, amount=Money(1.00)) 
  loan_info = LoanInfo(Money(10000.00), interest=1.00, start_date=accrue_start_date)

  return Loan(loan_info, bill_info)  


def test_not_accruing(current_date):
  """
  A loan that is not accruing should not chnage the total_owed
  of the loan.
  """
  accrue_start_date = current_date.date + datetime.timedelta(days=100)
  loan = create_loan(accrue_start_date) 

  intial_owed = loan.total_owed

  accruer = InterestAccruer(loan)

  current_date.register(accruer)
  current_date.increment_day()

  assert round(intial_owed, 2) == round(loan.total_owed, 2)


def test_accruing(current_date):
  """
  Total owed of a loan should change if loan is accruing.
  """
  loan = create_loan()

  intial_owed = loan.total_owed

  accruer = InterestAccruer(loan)

  current_date.register(accruer)
  current_date.increment_day()

  assert round(intial_owed, 2) != round(loan.total_owed, 2)


def test_loan_principal_increases(current_date):
  """
  Over the course of no more than 31 days the loan's principal
  must be increased by accrued interest.
  """
  loan = create_loan()
  initial_principal = loan.balance

  accruer = InterestAccruer(loan)
  current_date.register(accruer)

  balance_changed = False
  for i in range(31): # from 4th to 20
    current_date.increment_day()
    if loan.balance != initial_principal:
      balance_changed = True

  if balance_changed:
    assert True
  else:
    assert False


def test_loan_accrues_multiple_days(current_date):
  loan = create_loan()
  initial_principal = loan.balance
  accruer = InterestAccruer(loan)
  current_date.register(accruer)

  for i in range(10):
    current_date.increment_day()

  expected_interest = 10 * 1.00 * Money(10000.00) / 366. / 100 

  assert almost_equal(loan.total_owed, initial_principal + expected_interest)

