#!/usr/bin/env python3


import datetime

import pytest

from finance.finance.money import Money
from finance.finance.loan import Loan, LoanStatus
from finance.finance.datesubject import DateSubject


@pytest.fixture
def independence_day():
  """Create date subject for loan to watch."""
  date = datetime.date(2020, 7, 4)
  return DateSubject(date)

def test_create(independence_day):

  loan = Loan(Money(100.00), interest=1.00, bill_day=5, pay_day=10, 
              status=LoanStatus.IN_PROGRESS, min_payment=Money(10.00))

  
  assert False