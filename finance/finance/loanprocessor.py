

import datetime

from .billinfo import BillInfo
from .loan import Loan
from .loaninfo import LoanInfo
from .loanreader import LoanReader
from .money import Money


class LoanProcessor:
  """
  LoanReader class reads a text CSV file and creates a dictionary for each row.
  This class converts that data into a Loan instance.
  """
  def __init__(self, filename):
    loan_reader = LoanReader(filename)
    self._loan_data = loan_reader.read() # \todo need something to validate the data

  def _loan_datum_to_loan(self, datum):
    """Convert loanreader's data into Loan instances"""
    balance = Money(datum['balance'])
    interest = float(datum['interest rate'])
    bill_day = datum['bill day']
    pay_day = datum['pay day']
    min_payment = float(datum['minimum payment'])

    if datum['date billing starts'].strip() != 'None':
      date = datetime.datetime.strptime(datum['date billing starts'], "%m/%d/%Y").date()
      bill_info = BillInfo(bill_day, min_payment, False, date)
    else:
      bill_info = BillInfo(bill_day, min_payment)

    if datum['date accruing starts'].strip() != 'None':
      date = datetime.datetime.strptime(datum['date accruing starts'], "%m/%d/%Y").date()
      loan_info = LoanInfo(balance, interest, False, date)
    else:
      loan_info = LoanInfo(balance, interest)
    
    return Loan(loan_info, bill_info)

  def create_loans(self):
    loans = []
    for datum in self._loan_data:
      loans.append(self._loan_datum_to_loan(datum))

    return loans 
