

from .obsloan import Observer


class HighestInterestFirstPayer(observer):
  """
  A loan list observer.

  Given a collection of loans, this payer will always place money
  towards the highest interest loan (IN_PROGRESS) first.
  """
  def __init__(self, loan_list, account, pay_day):
    self._loan_list = loan_list
    self._account = account
    self._pay_day = _pay_day