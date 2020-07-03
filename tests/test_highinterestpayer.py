

import datetime

import pytest

from finance.finance.account import Account
from finance.finance.billinfo import BillInfo
from finance.finance.datesubject import DateSubject
from finance.finance.highinterestpayer import HighestInterestFirstPayer
from finance.finance.loan import Loan
from finance.finance.loaninfo import LoanInfo
from finance.finance.money import Money


@pytest.fixture
def current_date():
  """Create date subject for loan to watch."""
  date = datetime.date(2020, 7, 4)
  return DateSubject(date)


def test_zero_balance_loan(current_date):
  """
  If there is a zero balance loan total owed of highinterestpayer
  should remain zero, and account amount should be unchanged.
  """
  init_account_balance = Money(10000.00)
  account = Account(Money(10000.00))

  bill_info = BillInfo(day=10, amount=Money(1.00)) 
  loan_info = LoanInfo(Money(0.00), interest=1.00, accruing=True)

  loans = [Loan(loan_info, bill_info)]

  payer = HighestInterestFirstPayer(loans, account, 8, Money(10.00))
  init_total_owed = payer.total_owed

  current_date.register(payer)
  for i in range(31):
    current_date.increment_day()

  assert init_account_balance == account.balance
  assert init_total_owed == payer.total_owed


def test_nonzero_balance_loan(current_date):
  """
  If there is a nonzero balance loan total owed of highinterestpayer
  should change, and account amount should change.
  """
  init_account_balance = Money(10000.00)
  account = Account(Money(10000.00))

  bill_info = BillInfo(day=10, amount=Money(1.00)) 
  loan_info = LoanInfo(Money(100.00), interest=1.00, accruing=True)

  loans = [Loan(loan_info, bill_info)]

  payer = HighestInterestFirstPayer(loans, account, 8, Money(10.00))
  init_total_owed = payer.total_owed

  current_date.register(payer)
  for i in range(31):
    current_date.increment_day()

  assert init_account_balance != account.balance
  assert init_total_owed != payer.total_owed

  