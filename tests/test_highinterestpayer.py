

import datetime

import pytest

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


def test_dummy(current_date):
  assert False