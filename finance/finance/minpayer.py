

from .observer import Observer


class MinPaymentPayer(Observer):
  """
  A loan observer of the date.

  Given a loan with a required minimum payment, observe the current date.
  If the current date is the loan's bill cycle end date (bill_date),
  then make the minimum payment. Don't overpay if the loan's balance is
  less than the minimum payment.
  """
  def __init__(self, loan, account):
    self._loan = loan # the loan observing the date
    self._account = account


  def update(self, subject):
    """When date is incremented by a date, this function is called."""
    
  

