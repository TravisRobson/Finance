

from .observer import Observer

class StartAccruingObserver(Observer):
  """
  When the date which a loan billing starts, modify 
  loan data such that minimum payments are being made.
  """
  def __init__(self, loan):
    self._loan = loan

  def update(self, subject):
    if self._loan.accrue_start_date == subject.date:
      self._loan.accruing = True
