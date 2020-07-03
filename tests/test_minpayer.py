#!/usr/bin/env python3


import datetime

import pytest

from finance.finance.account import Account
from finance.finance.billinfo import BillInfo
from finance.finance.datesubject import DateSubject
from finance.finance.loan import Loan
from finance.finance.loaninfo import LoanInfo
from finance.finance.minpayer import MinPaymentPayer
from finance.finance.money import Money


@pytest.fixture
def current_date():
  """Create date subject for loan to watch."""
  date = datetime.date(2020, 7, 4)
  return DateSubject(date)

def test_not_in_progress(current_date):
  """
  If min payments are not in progress hitting bill date should
  not change account balance or total owed on loan.
  """
  initial_balance = Money(100.00)

  # create loan where minimum payment is the day after ptest fixture's date.
  bill_info = BillInfo(day=5, amount=Money(10.00), in_progress=False)
  loan_info = LoanInfo(initial_balance, interest=1.00)
  loan = Loan(loan_info, bill_info)

  initial_amount = Money(1000.00)
  account = Account(initial_amount) # a reserve of money
  payer = MinPaymentPayer(loan, account)

  current_date.register(payer)
  current_date.increment_day()
  assert account.balance == initial_amount
  assert loan.total_owed == initial_balance


def test_in_progress(current_date):
  """
  If min payments are in progress account balance should change, and
  loan balance should change.
  """
  initial_balance = Money(100.00)

  # create loan where minimum payment is the day after ptest fixture's date.
  bill_info = BillInfo(day=5, amount=Money(10.00), in_progress=True)
  loan_info = LoanInfo(initial_balance, interest=1.00)
  loan = Loan(loan_info, bill_info)

  initial_amount = Money(1000.00)
  account = Account(initial_amount) # a reserve of money
  payer = MinPaymentPayer(loan, account)

  current_date.register(payer)
  current_date.increment_day()
  assert account.balance != initial_amount
  assert loan.total_owed != initial_balance
