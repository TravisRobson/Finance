

from .money import Money


class LoanInfo:

  def __init__(self, balance, interest, accruing=True, start_date=None):
    """
    Interest rate is APR, assumed to be a percentage.
    """
    assert float(balance) > 0.0, "Loan balance must be postive."
    if not isinstance(balance, Money):
      balance = Money(balance)
    assert interest >= 0.0, "Interest rate must be non-negative"

    self._balance = round(balance, 2) # Ensure balance is rounded to pennies.
    self._interest = interest
    self._accruing = accruing
    self._start_date = start_date

  def __repr__(self):
    msg = (
      f"{self.__class__.__name__}("
      f"balance={self._balance}, "
      f"interest={self._interest}, "
      f"accruing={self._accruing}, "
      f"start date={self._start_date})"
    )
    return msg

  @property
  def balance(self):
    return self._balance

  @balance.setter
  def balance(self, val):
    self._balance = val

  @property
  def interest(self):
    return self._interest
  
  @property
  def accruing(self):
    return self._accruing

  @accruing.setter
  def accruing(self, val):
    self._accruing = val

  @property
  def start_date(self):
    return self._start_date


def call_with_non_none_args(func, *args, **kwargs):
  kwargs_not_none = {k: v for k, v in kwargs.items() if v is not None}
  return func(*args, **kwargs_not_none)


def create_loan_info(data_dict):
  """From dataparser.py data dictionary create a LoanInfo instance"""
  if 'balance' not in data_dict:
    raise ParserError('balance')
  if 'interest' not in data_dict:
    raise ParserError('interest')

  return call_with_non_none_args(LoanInfo,
    balance=data_dict['balance'], interest=data_dict['interest'], start_date=data_dict.get('start_date', None))
  
  
  