#!/usr/bin/env python3

import datetime
import multiprocessing

import numpy as np
import matplotlib.pyplot as plt

from .process import Process 
from .loanreader import LoanReader
from .money import Money
from .loan import Loan, LoanStatus, InvalidLoanStatus
from .obsloan import ObserverLoan
from .datesubject import DateSubject
from .loanutils import total_owed_on_loans
from .account import Account


def plot(x, y):
  fig, ax = plt.subplots(figsize=(4, 3), dpi=150)
  ax.plot(x, y / 1000, ls="-.")
  ax.set_title('Total owed on student loans')
  ax.set_xlabel('days')
  ax.set_ylabel('Money (1000 USD)')
  plt.tight_layout()
  plt.show()


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


  def loan_datum_to_loan(self, datum):
    """Convert loanreader's data into Loan instances"""
    balance = Money(datum['balance'])
    interest = float(datum['interest rate'])
    bill_day = datum['bill day']
    pay_day = datum['pay day']
    if datum['status'] == 'in progress':
      status = LoanStatus.IN_PROGRESS
    elif datum['status'] == 'forbearance':
      status = LoanStatus.FORBEARANCE
    elif datum['status'] == 'deferred':
      status = LoanStatus.DEFERRED
    else:
      raise InvalidLoanStatus(datum['status'])

    try:
      result = Loan(balance, interest, bill_day, pay_day, status)
    except:
      raise

    return result

  def run(self):
    """
    """

    account = Account(Money(1000000.00))



    loan_reader = LoanReader('etc/loans.csv')
    # loan_reader = LoanReader('etc/example_loans.csv')
    loan_data = loan_reader.read()
    # \todo need something to validate the data

    loans = []
    for datum in loan_data:
      loans.append(self.loan_datum_to_loan(datum))

    total = total_owed_on_loans(loans)
    print(f'Total balance {total}')


    # End date will trump num_days
    num_days = self.options.known.num_days
    today = datetime.datetime.today()
    if self.options.known.end_date:
      end_date = datetime.datetime.strptime(self.options.known.end_date, '%b %d %Y')
      num_days = (end_date - today).days


    days = np.arange(0, num_days, 1)
    totals = np.zeros(len(days))
    
    current_date = DateSubject(today)

    obs_loans = []
    for loan in loans:
      obs_loans.append(ObserverLoan(loan))

    for loan in obs_loans:
      current_date.register(loan)

    for day in range(num_days):
      current_date.increment_day()
      totals[day] = float(total_owed_on_loans(loans))

    if not self.options.known.disable_figure:
      proc = multiprocessing.Process(target=plot, args=(days, totals))
      proc.start()

    print(f'Total balance {total_owed_on_loans(loans)}')
