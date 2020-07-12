

from .exceptions import InvalidBillDayOfMonth
from .money import Money


class BillInfo():
  """Data about billing on a loan"""
  def __init__(self, day, amount, start_date=None):
    """
    If there is no start date provided the loan is assume to already be 
    billing the borrower.
    """
    if not InvalidBillDayOfMonth.is_valid(day):
      raise InvalidBillDayOfMonth

    if not isinstance(amount, Money):
      amount = Money(amount)

    self._day = int(day) # day the minimum payment is due
    self._amount = amount # min payment of a loan
    self._start_date = start_date

  def __repr__(self):
    msg = (
      f"{self.__class__.__name__}("
      f"day={self._day}, "
      f"amount={self._amount}, "
      f"start_date={self._start_date})"
    )
    return msg 

  def billing(self, date):
    result = True
    if self._start_date:
      result = date >= self._start_date
    return result

  @property
  def amount(self):
    return self._amount

  @property
  def day(self):
    return self._day

  @property
  def start_date(self):
    return self._start_date


def create_bill_info(data_dict):
  """From dataparser.py data dictionary create a BillInfo instance"""
  return BillInfo(data_dict['day'], data_dict['amount'])

