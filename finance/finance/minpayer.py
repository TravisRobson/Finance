

import datetime

from .observer import Observer


class MinPaymentPayer(Observer):
  """
  A loan observer of the date.

  Given a loan with a required minimum payment, observe the current date.
  If the current date is the loan's bill cycle end date (bill_date),
  then make the minimum payment. Don't overpay if the loan's balance is
  less than the minimum payment.
  """
  def __init__(self, loan, account):
    self._loan = loan # the loan observing the date
    self._account = account

  def _get_bill_date(self, subject):
    """Get bill-cycle date in same month as datesubject."""
    tt = subject.date.timetuple()
    return datetime.date(tt.tm_year, tt.tm_mon, self._loan.bill_day) 

  def update(self, subject):
    """When date is incremented by a date, this function is called."""
    if self._loan.total_owed and self._loan.bill_in_progress:
      bill_date = self._get_bill_date(subject) 

      if bill_date == subject.date:
        amount = min([self._loan.min_payment, self._loan.total_owed])

        self._account.remove_money(amount)
        self._loan.make_payment(amount)
  

