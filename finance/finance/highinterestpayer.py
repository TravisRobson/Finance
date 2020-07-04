

import datetime 

from .loan import Loan
from .loanutils import sort_high_interest_first
from .observer import Observer
from .money import Money


class HighestInterestFirstPayer(Observer):
  """
  A loan list observer.

  Given a collection of loans, this payer will always place money
  towards the highest interest loan (which are accruing) first.

  If there are no accruing loans, it will move on to non-accruing
  ones, again highest interest first.
  """
  def __init__(self, loans, account, day, amount): # \todo make bill info work here?
    self._loans = loans
    self._account = account
    self._day = day
    self._amount = amount

  def __str__(self):
    return str(self._loan)

  @property
  def total_owed(self):
    total_owed = Money(0.00)
    for l in self._loans:
      total_owed += l.total_owed
    return total_owed

  def _get_bill_date(self, subject):
    """Get bill-cycle date in same month as datesubject."""
    tt = subject.date.timetuple()
    return datetime.date(tt.tm_year, tt.tm_mon, self._day) 

  def _update_loans(self, loans):
    sorted_loans = sort_high_interest_first(loans)

    loan = sorted_loans[0]

    amount = min([self._amount, loan.total_owed])

    self._account.remove_money(amount)
    loan.make_payment(amount)

  def update(self, subject):
    """
    Attempts to use the full amount. If a loan is killed in the process
    the next highest interest loan is targeted.
    """
    bill_date = self._get_bill_date(subject)
    if bill_date == subject.date:
      nonzero_loans = [l for l in self._loans if l.total_owed != Money()]
      accruing_loans = [l for l in self._loans if l.accruing]
      self._update_loans(accruing_loans)
    


