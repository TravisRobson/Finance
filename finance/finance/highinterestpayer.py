

import datetime 

from .dataparser import ParserError
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
    if not isinstance(amount, Money):
      amount = Money(amount)
    self._amount = amount

  def __str__(self):
    return str(self._loan)

  @property
  def total_owed(self):
    total_owed = Money(0.00)
    for l in self._loans:
      total_owed += l.total_owed
    return total_owed

  @property
  def amount(self):
    return self._amount
  
  @amount.setter
  def amount(self, val):
    self._amount = val

  def _get_bill_date(self, subject):
    """Get bill-cycle date in same month as datesubject."""
    tt = subject.date.timetuple()
    return datetime.date(tt.tm_year, tt.tm_mon, self._day) 

  def _update_loans(self, loans, payment_amount):
    sorted_loans = sort_high_interest_first(loans)
    
    index = 0
    amount_left = payment_amount
    while amount_left > Money(0.00) and index < len(loans):
      loan = sorted_loans[index]
      amount = min(amount_left, loan.total_owed)

      self._account.remove_money(amount)
      loan.make_payment(amount)

      amount_left -= amount
      index += 1

    return amount_left

  def update(self, subject):
    """
    Attempts to use the full amount. If a loan is killed in the process
    the next highest interest loan is targeted.
    """
    bill_date = self._get_bill_date(subject)
    if bill_date == subject.date:
      nonzero_loans = [l for l in self._loans if l.total_owed != Money()]
      accruing_loans = [l for l in nonzero_loans if l.accruing(subject.date)]
      amount_left = self._update_loans(accruing_loans, self._amount)

      if amount_left > Money(0.00):
        nonacrruing_loans = [l for l in nonzero_loans if not l.accruing(subject.date)]
        self._update_loans(nonacrruing_loans, amount_left)
    

def create_payers(data_dict, loans, account):
  """
  dataparser.py will parse the data file to create a dictionary of data 
  which this function turns into a loan.
  """
  payers = []
  for d in data_dict:
    if 'amount' not in d:
      raise ParserError('amount')
    if 'start date' not in d:
      raise ParserError('start date')

    amount = d['amount']
    # NEED TO DO SOME VALIDATION ON THE DAY
    start_date = datetime.datetime.strptime(d['start date'], "%m-%d-%Y").date()

    payers.append(HighestInterestFirstPayer(loans, account, start_date.day, amount))

  return payers
