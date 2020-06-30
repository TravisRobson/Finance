

import datetime 

from .loan import Loan
from .obsloan import Observer


class HighestInterestFirstPayer(Observer):
  """
  A loan list observer.

  Given a collection of loans, this payer will always place money
  towards the highest interest loan (IN_PROGRESS) first.
  """
  def __init__(self, loan_list, account, pay_day, amount_per_payment):
    self._loan_list = loan_list
    self._account = account
    self._pay_day = pay_day
    self._amount_per_payment = amount_per_payment

  def update(self, subject):
    tt = subject.date.timetuple()
    pay_date = datetime.date(tt.tm_year, tt.tm_mon, self._pay_day)

    sorted_loans = sorted(self._loan_list, key=lambda x: x.interest)
    if pay_date == subject.date.date():
      self._account.remove_money(self._amount_per_payment)
      sorted_loans[0].apply_money(self._amount_per_payment)