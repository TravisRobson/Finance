

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
    return datetime.date(tt.tm_year, tt.tm_mon, self._loan.bill_day) 

  def _update_accruing_loans(self, loans):
    accruing_loans = [l for l in loans if l.accruing]
    sorted_loans = sort_high_interest_first(accruing_loans)
    

  def update(self, subject):
    """
    Attempts to use the full amount. If a loan is killed in the process
    the next highest interest loan is targeted.
    """
    nonzero_loans = [l for l in self._loans if l.total_owed != Money()]

    self._update_accruing_loans(nonzero_loans)
    

    # # sorted_loans = sorted(self._loan_list, key=lambda x: x.interest, reverse=True)

    # sorted_loans = sorted(non_zero_loans, key=lambda x: x.interest, reverse=True)

    # idx = 0
    # if pay_date == subject.date.date() and sorted_loans:

    #   current_loan = sorted_loans[idx]

    #   amount = self._amount_per_payment
    #   while amount.__round__(2) > Money().__round__(2):

    #     non_zero_loans = [l for l in self._loan_list if l.total_owed != Money()]
    #     sorted_loans = sorted(non_zero_loans, key=lambda x: x.interest, reverse=True)
    #     if not sorted_loans:
    #       return
    #     print(f"{amount.__repr__()}")
    #     amount_to_pay = amount

    #     if amount_to_pay > current_loan.total_owed:
    #       amount_to_pay = current_loan.total_owed
    #       amount -= current_loan.total_owed
    #       idx += 1
    #       if idx == len(non_zero_loans):
    #         return
    #       # if idx >= len(sorted_loans):
    #       #   return
    #     else:
    #       amount = Money()

    #     print(f"{amount_to_pay}, {current_loan.total_owed}, {amount.__repr__() > Money().__repr__()}")

    #     self._account.remove_money(amount_to_pay)
    #     current_loan.apply_money(amount_to_pay)
