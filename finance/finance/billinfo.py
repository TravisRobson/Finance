

import enum

from .exceptions import InvalidBillDayOfMonth
from .money import Money


class BillInfo():
  """Data about billing on a loan"""
  def __init__(self, day, amount, in_progress=True):
    """Validate args and set member variables"""
    if not InvalidBillDayOfMonth.is_valid(day):
      raise InvalidBillDayOfMonth

    if not isinstance(amount, Money):
      amount = Money(amount)

    self._day = int(day) # day the minimum payment is due
    self._amount = amount # min payment of a loan
    self._in_progress = in_progress # Is the bill being collected or is loan in deferrment?

  def __str__(self):
    return f"Bill day: {self._day}, amount: {self._amount}, in progress: {self._in_progress}"

  def __repr__(self):
    return f"{repr(self._day)}, {repr(self._amount)}, {repr(self._in_progress)}"

  @property
  def in_progress(self):
    return self._in_progress
  
  @property
  def amount(self):
    return self._amount

  @property
  def day(self):
    return self._day
