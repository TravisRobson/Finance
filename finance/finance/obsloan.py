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


  def __str__(self):
    return str(self._loan)


  @property
  def total_owed(self):
    return self._loan.total_owed
  

  def update(self, subject):
    if self.total_owed:
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

        amount = self._loan.min_payment
        if amount > self._loan.total_owed:
          amount = self._loan.total_owed

        self._account.remove_money(amount)
        self._loan.apply_money(amount)


      