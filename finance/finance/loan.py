#!/usr/bin/env python3

from enum import Enum

from .money import Money


class LoanStatus(Enum):
  IN_PROGRESS = 1
  DEFERRED = 2
  FORBEARANCE = 3


class Loan:

  def __init__(self, balance, interest, bill_day_of_month, pay_day_of_month, status):
    if balance < 0.0:
      raise NegativeLoanBalance()
    if not 1 < int(bill_day_of_month) < 28: # \todo is it really 28 ya think?
      raise InvalidDayOfMonth(bill_day_of_month)
    if not 1 < int(pay_day_of_month) < 28: 
      raise InvalidDayOfMonth(pay_day_of_month)

    self._balance = balance.__round__(2)
    self._interest = interest # APR
    self._bill_day_of_month = int(bill_day_of_month)
    self._pay_day_of_month = int(pay_day_of_month)
    self._status = status

  def __str__(self):
    return f"${self._balance}, {self._interest}%, bill day: {self._bill_day_of_month}, pay day: {self._pay_day_of_month}, {self._status}"
 
  def __repr__(self):
    return f"{self._balance}, {self._interest}, {self._bill_day_of_month}, {self._pay_day_of_month}, {self._status}"

  @property
  def balance(self):
    return self._balance

  
class InvalidDayOfMonth(Exception):

  def __init__(self, value):
    self._value = value

  def __str__(self):
    return f"value ({self._value})"


class NegativeLoanBalance(Exception):
  def __init__(self):
    pass



