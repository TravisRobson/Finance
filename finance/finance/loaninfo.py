

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

  def __str__(self):
    return f"balance: {self._balance}, interest: {self._interest}, accruing: {self._accruing}"

  def __repr__(self):
    return f"{repr(self._balance)}, {repr(self._interest)}, {repr(self._accruing)}"

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
  
  
  