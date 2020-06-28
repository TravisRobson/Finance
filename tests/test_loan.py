#!/usr/bin/env python3


from datetime import time
from decimal import Decimal
from unittest import TestCase

import pytest

from finance.finance.money import Money
from finance.finance.loan import Loan, InvalidLoanBalance


@pytest.mark.parametrize("balance", [
  (Money(0.00)),
  (Money(-10.00)),
])
def test_init_raise_exception_invalid_balance(balance):
  with pytest.raises(InvalidLoanBalance):
    loan = Loan(balance, 0.00, 1, 1)



@pytest.fixture
def zero_accured_loan():
  """Return a loan with zero accrued interest"""
  return Loan(Money(100.00), interest=1.00, bill_day_of_month=1, pay_day_of_month=1)


@pytest.mark.parametrize("amount, expected", [
  (Money(1.00), Money(99.00)),
  (Money(5.00), Money(95.00)),
  (Money(67), Money(33))
])
def test_apply_money(zero_accured_loan, amount, expected):
  zero_accured_loan.apply_money(amount)
  assert zero_accured_loan.balance == expected
