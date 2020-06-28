#!/usr/bin/env python3


import datetime
from decimal import Decimal
from unittest import TestCase
from random import randint

import pytest

from finance.finance.money import Money, almost_equal
from finance.finance.loan import Loan, InvalidLoanBalance


@pytest.mark.parametrize("balance", [
  (Money(0.00)),
  (Money(-10.00)),
])
def test_init_raise_exception_invalid_balance(balance):
  """Loans cannot have non-positive balances"""
  with pytest.raises(InvalidLoanBalance):
    loan = Loan(balance, 0.00, 1, 1)


@pytest.fixture
def zero_accured_loan():
  """Return a loan with zero accrued interest with 1% interest rate (APR)"""
  return Loan(Money(100.00), interest=1.00, bill_day_of_month=1, pay_day_of_month=1)


@pytest.mark.parametrize("amount, expected", [
  (Money(1.00), Money(99.00)),
  (Money(5.00), Money(95.00)),
  (Money(67), Money(33))
])
def test_apply_money(zero_accured_loan, amount, expected):
  """If you apply $1 to a loan, its balance should descrease by $1"""
  zero_accured_loan.apply_money(amount)
  assert zero_accured_loan.balance == expected


@pytest.mark.parametrize("num_days", [randint(0, 1000) for i in range(10)]) 
def test_daily_accrued(zero_accured_loan, num_days):
  """
  If you have a 1% APR and accrue the daily interest rate 365 times 
  on a $100 balance loan, the accured interest should be $1.
  """
  date = datetime.date(2011, 1, 1)
  for i in range(num_days):
    zero_accured_loan.accrue_daily(date.timetuple().tm_year)
  assert almost_equal(zero_accured_loan.total_owed, Money(100.00 + num_days / 365))


