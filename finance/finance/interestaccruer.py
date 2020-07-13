
import datetime

from .exceptions import InvalidBillDayOfMonth
from .observer import Observer


class InterestAccruer:

  def __init__(self, loan):
    self._loan = loan

  def _get_bill_date(self, subject):
    """Get bill-cycle date in same month as datesubject."""
    tt = subject.date.timetuple()
    return datetime.date(tt.tm_year, tt.tm_mon, self._loan.bill_day) 

  def update(self, subject):
    """Every day, daily interest is accrued."""
    if self._loan.accruing(subject.date) and self._loan.total_owed:
      self._loan.accrue_daily(subject.year)

      bill_date = self._get_bill_date(subject) 
      if bill_date == subject.date:
        self._loan.convert_accrued_to_principal()
      