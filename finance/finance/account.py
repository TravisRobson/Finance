

from .money import Money


class InsufficientFunds(Exception):
  pass


class Account:
  """Like a checking account. Simply a reserve of money."""
  def __init__(self, balance=Money()):
    self._balance = balance

  def __str__(self):
    return f"{self.balance}"

  @property
  def balance(self):
    return self._balance
  
  def remove_money(self, amount):
    if amount > self._balance:
      raise InsufficientFunds
    else:
      self._balance -= amount

