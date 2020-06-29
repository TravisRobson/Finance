#!/usr/bin/env python3


import pytest

from finance.finance.loan import Loan
from finance.finance.obsloan import ObserverLoan
from finance.finance.datesubject import DateSubject

import datetime


def test_foo():
  date = datetime.date(2020, 6, 25)
  working_date = DateSubject(date)


  loan = Loan(100.00, 1.0, 27, 15)
  obs_loan = ObserverLoan(loan)

  working_date.register(obs_loan)

  # 25th to 26th
  working_date.increment_day()

  # 26th to 27th i.e. pay up!
  working_date.increment_day()

  assert True
