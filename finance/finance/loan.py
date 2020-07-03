#!/usr/bin/env python3

import calendar
import decimal

from .money import Money
from .exceptions import InvalidBillDayOfMonth


class InvalidLoanBalance(Exception):

  def __init__(self, amount):
    self._amount = amount

  def __str__(self):
    return f"amount {self._amount}, must be > $0.00"


class InvalidLoanStatus(Exception):
  def __init__(self, status):
    self._status = status
  def __str__(self):
    return f"Invalid loan status read ({self._status})"


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


class Loan: # \todo perhaps name SimpleDailyLoan

  def __init__(self, balance, interest, pay_day, bill_info):
    """
    Interest rate is APR, assumed to be a percentage.

    I am going to assume simple daily interest loan
    """
    self._validate_args(balance, pay_day)

    # convert floats to money
    if not isinstance(balance, Money): 
      balance = Money(balance)

    self._balance = balance.__round__(2) # Ensure balance is rounded to pennies.
    self._interest = interest # APR
    self._pay_day = int(pay_day)
    self._bill_info = bill_info
    self._accrued_interest = Money(0.00)

  def _validate_args(balance, pay_day):
    if not balance > 0.0:
      raise InvalidLoanBalance(balance)

    if not InvalidBillDayOfMonth.isValid(pay_day):
      raise InvalidBillDayOfMonth(pay_day)

  def __str__(self):
    msg = (
      f"{self._balance}, {self._interest}%, {self._accrued_interest}, "
      f"bill info: {self._bill_info}, "
      f"pay day: {self._pay_day}"
    )
    return msg
 
  def __repr__(self):
    return f"{self._balance}, {self._interest}, {self._accrued_interest}, {self._bill_info}, {self._pay_day}"

  @property
  def balance(self):
    return self._balance

  @property
  def total_owed(self):
    return self._balance + self._accrued_interest
  
  @property
  def bill_day(self):
    return self._bill_info.day

  @property
  def pay_day(self):
    return self._pay_day

  @property
  def min_payment(self):
    return self._bill_info.min_amount

  @property
  def status(self):
    return self._bill_info.in_progress

  @property
  def interest(self):
    return self._interest

  def accrue_daily(self, year) -> None:
    # get current month from date
    if self._status != LoanStatus.FORBEARANCE:
      num_days_in_year = 365
      if calendar.isleap(year):
        num_days_in_year = 366

      daily_interest_rate = decimal.Decimal(self._interest / 100.00 / num_days_in_year)
      self._accrued_interest += daily_interest_rate * self._balance 

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

  def convert_accrued_to_principal(self) -> None:
    self._balance += self._accrued_interest
    self._accrued_interest = Money()
