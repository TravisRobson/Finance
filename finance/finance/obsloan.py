#!/usr/bin/env python3



import datetime

from .loan import LoanStatus
from .observer import Observer


# \todo convert this to InterestAccruer, and break out min_payment payer
class ObserverLoan(Observer):
  """
  Responsible for watching the date, accruing interest on bill day,
  and paying minimums when pay day comes (pay day of loan).
  """
  def __init__(self, loan, account=None):
    self._loan = loan
    self._account = account # the account which to take payments from

  def update(self, subject):
    tt = subject.date.timetuple()
    bill_date = datetime.date(tt.tm_year, tt.tm_mon, self._loan.bill_day) 
    self._loan.accrue_daily(tt.tm_year)

    if bill_date == subject.date.date():
      self._loan.convert_accrued_to_principal()

    pay_date = datetime.date(tt.tm_year, tt.tm_mon, self._loan.pay_day) 

    todayIsPayDay = pay_date == subject.date.date()
    loanInProgress = self._loan.status == LoanStatus.IN_PROGRESS
    makePayment = self._account and todayIsPayDay and loanInProgress

    if makePayment:
      self._account.remove_money(self._loan.min_payment)
      self._loan.apply_money(self._loan.min_payment)

      