

import calendar
import decimal

from .billinfo import BillInfo, create_bill_info
from .exceptions import FinanceError
from .loaninfo import LoanInfo, create_loan_info
from .dataparser import ParserError
from .money import Money


class ExcessivePaymentError(FinanceError):

  def __init__(self, balance, accrued, amount):
    msg = (
      f"Excessive payment of {amount} on loan with balance {balance} and "
      f"accrued interest {accrued}"
    )
    super(ExcessivePaymentError, self).__init__(msg)
    self._balance = balance
    self._accrued = accrued
    self._amount = amount


class Loan: 

  def __init__(self, loan_info, bill_info):
    """
    Assume simple daily interest loan.
    """
    self._loan_info = loan_info
    self._bill_info = bill_info
    self._accrued_interest = Money(0.00)

  def __str__(self):
    msg = (
      f"{self.__class__.__name__}("
      f"loan_info={self._loan_info}, "
      f"bill_info={self._bill_info}, "
      f"accrued_interest={self._accrued_interest})"
    )
    return msg
 
  def __repr__(self):
    return str(self)

  @property
  def balance(self):
    return self._loan_info.balance

  @property
  def total_owed(self):
    return self._loan_info.balance + self._accrued_interest
  
  @property
  def bill_day(self):
    return self._bill_info.day

  @property
  def min_payment(self):
    return self._bill_info.amount

  @property
  def interest(self):
    return self._loan_info.interest

  @property
  def accruing(self):
    return self._loan_info.accruing

  @accruing.setter
  def accruing(self, val):
    self._loan_info.accruing = val

  @property
  def accrued_interest(self):
    return self._accrued_interest
  
  def billing(self, date):
    return self._bill_info.billing(date)
  
  @property
  def bill_start_date(self):
    return self._bill_info.start_date

  @property
  def accrue_start_date(self):
    return self._loan_info.start_date
  
  def _calc_daily_interest(self, year):
    num_days_in_year = 365
    if calendar.isleap(year):
      num_days_in_year = 366

    return decimal.Decimal(self.interest / 100.00 / num_days_in_year)

  def accrue_daily(self, year) -> None:
    if self.accruing:
      self._accrued_interest += self._calc_daily_interest(year) * self.balance 

  def make_payment(self, amount) -> None:
    """
    It is the reponsibility of the user to not attempt to pay more 
    than what is owed.
    """
    if amount > self.total_owed:
      raise ExcessivePaymentError(self.balance, self.accrued_interest, amount)

    leftover = self._apply_to_accrued(amount) # you must pay on accrued interest first

    if leftover and not self._accrued_interest:
      self._loan_info.balance -= leftover
      self._loan_info.balance = round(self._loan_info.balance)

  def _apply_to_accrued(self, amount) -> None:
    accrued = self._accrued_interest
    if amount <= accrued:
      self._accrued_interest -= amount
      self._accrued_interest = round(self._accrued_interest)
      return Money(0.00)
    else:
      self._accrued_interest = Money(0.00)
      return amount - accrued

  def convert_accrued_to_principal(self) -> None:
    self._loan_info.balance += self._accrued_interest
    self._loan_info.balance = round(self._loan_info.balance)
    self._accrued_interest = Money(0.00)


def create_loans(data_dict):
  """
  dataparser.py will parse the data file to create a dictionary of data 
  which this function turns into a loan.
  """
  loans = []
  for d in data_dict:
    if 'loan info' not in d:
      raise ParserError('loan info')
    if 'bill info' not in d:
      raise ParserError('bill info')

    loan_info_data = d['loan info']
    bill_info_data = d['bill info']

    loans.append(Loan(create_loan_info(loan_info_data), create_bill_info(bill_info_data)))

  return loans

