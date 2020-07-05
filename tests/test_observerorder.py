

import copy
import datetime

import pytest

from finance.finance.account import Account
from finance.finance.billinfo import BillInfo
from finance.finance.datesubject import DateSubject
from finance.finance.interestaccruer import InterestAccruer
from finance.finance.loan import Loan
from finance.finance.loaninfo import LoanInfo
from finance.finance.minpayer import MinPaymentPayer
from finance.finance.money import Money, almost_equal

def date_range(start, end):
  for i in range(int((end - start).days)):
    yield start + datetime.timedelta(days=i)

def test_order_observers_regiester():
  """
  The order in which two observers are registered should not affect
  the update cycle.
  """
  start = datetime.date(2020, 7, 4)
  date = DateSubject(start)
  end = date.date + datetime.timedelta(days=10)
  bill_info = BillInfo(day=end.day, amount=Money(10.00)) 
  loan_info = LoanInfo(Money(1000.00), interest=1.00)

  loan = Loan(loan_info, bill_info)
  loan_copy = copy.deepcopy(loan)

  account = Account(Money(10000.00)) # a reserve of money

  date.register(MinPaymentPayer(loan, account))
  date.register(InterestAccruer(loan))

  date.register(InterestAccruer(loan_copy))
  date.register(MinPaymentPayer(loan_copy, account))

  for d in date_range(start, end):
    date.increment_day()

  assert almost_equal(loan.balance, loan_copy.balance)
  assert almost_equal(loan.total_owed, loan_copy.total_owed)

