

from .exceptions import FinanceError
from .dataparser import ParserError
from .money import Money


class InsufficientFundsError(FinanceError):

  def __init__(self, balance, amount):
    msg = f"Account balance {balance} insufficient for requested amount {amount}"
    super(InsufficientFundsError, self).__init__(msg)
    self.balance = balance
    self.amount = amount


class Account:
  """Like a checking account. Simply a reserve of money."""
  def __init__(self, balance=Money()):
    if not isinstance(balance, Money):
      balance = Money(balance)
    self._balance = balance

  def __str__(self):
    return f"{self.__class__.__name__}({self.balance})"

  @property
  def balance(self):
    return self._balance
  
  def remove_money(self, amount):
    if amount > self._balance:
      raise InsufficientFundsError(self._balance, amount)
    else:
      self._balance -= amount


def create_account(data_dict):
  """From dataparser.py data dictionary create a Account instance"""
  if 'balance' not in data_dict:
    raise ParserError('balance')
    
  return Account(data_dict['balance'])
