

from .money import Money


class InsufficientFunds(Exception):
  pass


class Account:
  """Like a checking account. Simply a reserve of money."""
  def __init__(self, balance=Money()):
    self._balance = balance

  def remove_money(self, amount):
    if amount > self._balance:
      raise InsufficientFunds
    else:
      self._balance -= amount

