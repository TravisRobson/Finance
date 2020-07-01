

import datetime 

from .loan import Loan
from .obsloan import Observer
from .money import Money


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

  def __str__(self):
    return str(self._loan)

  @property
  def total_owed(self):
    return self._loan.total_owed

  def update(self, subject):
    """
    Attempts to use the full amount. If a loan is killed in the process
    the next highest interest loan is targeted.
    """
    tt = subject.date.timetuple()
    pay_date = datetime.date(tt.tm_year, tt.tm_mon, self._pay_day)

    sorted_loans = sorted(self._loan_list, key=lambda x: x.interest, reverse=True)

    idx = 0
    if pay_date == subject.date.date() and sorted_loans:

      amount = self._amount_per_payment
      while amount > Money():

        amount_to_pay = amount

        if amount_to_pay > sorted_loans[idx].total_owed:
          amount_to_pay = sorted_loans[idx].total_owed
          amount -= sorted_loans[idx].total_owed
          idx += 1
          # if idx >= len(sorted_loans):
          #   return
        else:
          amount = Money()

        self._account.remove_money(amount_to_pay)
        sorted_loans[idx].apply_money(amount_to_pay)
