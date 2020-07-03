

import enum

from .exceptions import InvalidBillDayOfMonth
from .money import Money


class BillInfo():
  """Data about billing on a loan"""
  def __init__(self, day, min_amount, in_progress=True):
    """Validate args and set member variables"""
    if not InvalidBillDayOfMonth.is_valid(day):
      raise InvalidBillDayOfMonth

    if not isinstance(min_amount, Money):
      min_amount = Money(min_amount)

    self._day = day # day the minimum payment is due
    self._min_amount = min_amount # min payment of a loan
    self._in_progress = in_progress # Is the bill being collected or is loan in deferrment?

  def __str__(self):
    return f"Bill day: {self._day}, min amount: {self._min_amount}, in progress: {self._in_progress}"

  def __repr__(self):
    return f"{repr(self._day)}, {repr(self._min_amount)}, {repr(self._in_progress)}"

  @property
  def in_progress(self):
    return self._in_progress
  
  @property
  def min_amount(self):
    return self._min_amount

  @property
  def date(self):
    return self._day
