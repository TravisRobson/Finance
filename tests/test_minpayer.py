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


def create_loan(initial_amount, min_payment, in_progress=True):
  # create loan where minimum payment is the day after ptest fixture's date.
  bill_info = BillInfo(day=5, amount=min_payment, in_progress=in_progress) 
  loan_info = LoanInfo(initial_amount, interest=1.00)

  return Loan(loan_info, bill_info)


def test_not_in_progress(current_date):
  """
  If min payments are not in progress hitting bill date should
  not change account balance or total owed on loan.
  """
  initial_balance = Money(100.00)
  loan = create_loan(initial_balance, Money(10.00), False)

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
  loan = create_loan(initial_balance, Money(10.00))

  initial_amount = Money(1000.00)
  account = Account(initial_amount) # a reserve of money
  payer = MinPaymentPayer(loan, account)

  current_date.register(payer)
  current_date.increment_day()
  assert account.balance != initial_amount
  assert loan.total_owed != initial_balance


@pytest.mark.parametrize("min_payment", [Money(1.00), Money(5.34), Money(25.00)])
def test_payment_reduces_balance(current_date, min_payment):
  """
  When bill day is hit, loan total_owed reduces 
  by the minimum payment amount. Same with account balance.
  """
  initial_balance = Money(100.00)
  loan = create_loan(initial_balance, min_payment)

  initial_amount = Money(1000.00)
  account = Account(initial_amount) # a reserve of money
  payer = MinPaymentPayer(loan, account)

  current_date.register(payer)
  current_date.increment_day()
  assert account.balance == initial_amount - min_payment
  assert loan.total_owed == initial_balance - min_payment

@pytest.mark.parametrize("min_payment", [Money(101.00), Money(105.34), Money(250.00)])
def test_payment_reduces_balance(current_date, min_payment):
  """
  When bill day is hit, loan total_owed reduces to zero
  when minimum payment exceed amount owed on loan.
  """
  initial_balance = Money(100.00)
  loan = create_loan(initial_balance, min_payment)

  initial_amount = Money(1000.00)
  account = Account(initial_amount) # a reserve of money
  payer = MinPaymentPayer(loan, account)

  current_date.register(payer)
  current_date.increment_day()
  assert account.balance == initial_amount - initial_balance
  assert loan.total_owed == Money(0.00)
