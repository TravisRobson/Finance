#!/usr/bin/env python3

import enum
import calendar
import decimal

from .money import Money


class LoanStatus(enum.Enum):
  IN_PROGRESS = 1
  DEFERRED = 2
  FORBEARANCE = 3

class InvalidDayOfMonth(Exception):

  def __init__(self, value):
    self._value = value

  def __str__(self):
    return f"value ({self._value})"


class InvalidLoanBalance(Exception):

  def __init__(self, amount):
    self._amount = amount

  def __str__(self):
    return f"amount ${self._amount}, must be > $0.00"


class ExcessivePayment(Exception):

  def __init__(self, balance, accrued, amount):
    self._balance = balance
    self._accrued = accrued
    self._amount = amount

  def __str__(self):
    msg = (
      f"Amounted to pay ${self._amount} on loan "
      f"with balance ${self._balance}, "
      f"and accrued interest ${self._accrued}"
    )
    return msg


class Loan:

  def __init__(self, balance, interest, bill_day_of_month, pay_day_of_month, status=LoanStatus.IN_PROGRESS):
    """
    Interest rate is APR, assumed to be a percentage.
    """
    # validate
    if not balance > 0.0:
      raise InvalidLoanBalance(balance)
    self.validate_day_of_month(bill_day_of_month)
    self.validate_day_of_month(pay_day_of_month)

    # set values
    self._balance = balance.__round__(2)
    self._interest = interest # APR
    self._bill_day_of_month = int(bill_day_of_month)
    self._pay_day_of_month = int(pay_day_of_month)
    self._status = status
    self._accrued_interest = Money(0.00)

  def __str__(self):
    msg = (
      f"${self._balance}, {self._interest}%, ${self._accrued_interest}"
      f"bill day: {self._bill_day_of_month},"
      f"pay day: {self._pay_day_of_month}, {self._status}"
    )
    return msg
 
  def __repr__(self):
    return f"{self._balance}, {self._interest}, {self._accrued_interest}, {self._bill_day_of_month}, {self._pay_day_of_month}, {self._status}"

  @property
  def balance(self):
    return self._balance

  @property
  def total_owed(self):
    return self._balance + self._accrued_interest
  
  @property
  def bill_day_of_month(self):
    return self._bill_day_of_month
  


  def validate_day_of_month(self, day):
    """
    Max of 28 because you can't have a recurring date which doesn't fall
    within a non-leap year February.
    """
    if not 1 <= int(day) <= 28: 
      raise InvalidDayOfMonth(day)

  def accrue_daily(self, year) -> None:
    # get current month from date
    if self._status != LoanStatus.FORBEARANCE:
      num_days_in_year = 365
      if calendar.isleap(year):
        num_days_in_year = 366

      daily_interest_rate = decimal.Decimal(self._interest / 100.00 / num_days_in_year)
      self._accrued_interest += self._balance * daily_interest_rate 

  def apply_money(self, amount) -> None:
    """
    It is the reponsibility of the user to not attempt to pay more 
    than what is owed.
    """
    if amount > self.total_owed:
      raise ExcessivePayment(self._balance, self._accrued_interest, amount)
    else:
      # you must pay on accrued interest first
      leftover = self._apply_to_accrued(amount)
      if self._accrued_interest > 0.0: # i.e. still interest left to pay
        return
      else:
        self._balance -= leftover

  def _apply_to_accrued(self, amount) -> None:
    if amount <= self._accrued_interest:
      self._accrued_interest -= amount
      return Money(0.00)
    else:
      self._accrued_interest = Money(0.00)
      return amount - self._accrued_interest


  def convert_accrued_to_principal(self):
    pass
    


  




