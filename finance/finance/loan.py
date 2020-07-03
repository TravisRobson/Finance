#!/usr/bin/env python3

import calendar
import decimal

from .loaninfo import LoanInfo
from .money import Money
from .exceptions import InvalidBillDayOfMonth


class ExcessivePayment(Exception):

  def __init__(self, balance, accrued, amount):
    self._balance = balance
    self._accrued = accrued
    self._amount = amount

  def __str__(self):
    msg = (
      f"Amounted to pay {self._amount} on loan "
      f"with balance {self._balance}, "
      f"and accrued interest {self._accrued}"
    )
    return msg


class Loan: 

  def __init__(self, loan_info, bill_info):
    """
    Assume simple daily interest loan.
    """
    self._loan_info = loan_info
    self._bill_info = bill_info
    self._accrued_interest = Money(0.00)

  def __str__(self):
    msg = (
      f"loan info: {self._loan_info}, accrued interest: {self._accrued_interest}, "
      f"bill info: {self._bill_info}, "
    )
    return msg
 
  def __repr__(self):
    return f"{repr(self._loan_info)}, {rer(self._bill_info)}, {repr(self._accrued_interest)}"

  @property
  def balance(self):
    return self._loan_info.balance

  @property
  def total_owed(self):
    return self._loan_info.balance + self._accrued_interest
  
  @property
  def bill_day(self):
    return self._bill_info.day

  @property
  def min_payment(self):
    return self._bill_info.amount

  @property
  def interest(self):
    return self._loan_info.interest

  @property
  def accruing(self):
    return self._loan_info.accruing

  @property
  def bill_in_progress(self):
    return self._bill_info.in_progress

  def accrue_daily(self, year) -> None:
    # get current month from date
    if self.accruing:
      num_days_in_year = 365
      if calendar.isleap(year):
        num_days_in_year = 366

      daily_interest_rate = decimal.Decimal(self.interest / 100.00 / num_days_in_year)
      self._accrued_interest += daily_interest_rate * self.balance 

  def apply_money(self, amount) -> None:
    """
    It is the reponsibility of the user to not attempt to pay more 
    than what is owed.
    """
    if amount > self.total_owed:
      raise ExcessivePayment(self.balance, self.accrued_interest, amount)
    else:
      # you must pay on accrued interest first
      leftover = self._apply_to_accrued(amount)
      if self._accrued_interest > 0.0: # i.e. still interest left to pay
        return
      else:
        self._loan_info.balance -= leftover

  def _apply_to_accrued(self, amount) -> None:
    if amount <= self._accrued_interest:
      self._accrued_interest -= amount
      return Money(0.00)
    else:
      self._accrued_interest = Money(0.00)
      return amount - self._accrued_interest

  def convert_accrued_to_principal(self) -> None:
    self._loan_info.balance += self._accrued_interest
    self._accrued_interest = Money(0.00)
