#!/usr/bin/env python3

from logging import getLogger

from .process import Process # \todo need to figure out why I must prepend . to module names
from .loanreader import LoanReader
from .money import Money
from .loan import Loan, LoanStatus

class Finance:

  def __init__(self, options):
    self.options = options
    self.process = Process()


  def list_csv_files(self):
    return self._get_csv_files()


  def _get_csv_files(self):
    """
    List the *.csv files inside the etc/ folder

    Right now this is merely serving the purpose of an example for the 
    class that can run subprocesses
    """
    return self.process.run("ls etc/*.csv" ).decode('utf-8') 


  def run(self):
    """
    """
    #print(f"CSV files: {self.list_csv_files()}")

    loan_reader = LoanReader('etc/loans.csv')

    loan_data = loan_reader.read()

    # \todo need something to validate the data

    total = Money()

    for loan in loan_data:
      for key, value in loan.items():
        if key.strip() == 'balance':
          total += float(value)

    print(f'Total balance ${total}')

    first_loan = loan_data[1]

    balance = Money(first_loan['balance'].strip())
    interest = first_loan['interest rate'].strip()
    bill_day_of_month = first_loan['bill date'].strip()
    pay_day_of_month = first_loan['pay date'].strip()
    status_str = first_loan['status'].strip()
    if status_str == 'in progress':
      status = LoanStatus.IN_PROGRESS
    elif status_str == 'forbearance':
      status = LoanStatus.FORBEARANCE
    elif status_str == 'deferred':
      status = LoanStatus.DEFERRED
    else:
      raise Exception("Invalid loan status")

    loan = Loan(balance, interest, bill_day_of_month, pay_day_of_month, status)

    print(loan)








  