#!/usr/bin/env python3

import datetime
import multiprocessing

import numpy as np
import matplotlib.pyplot as plt

from .account import Account
from .billinfo import BillInfo
from .datesubject import DateSubject
from .highinterestpayer import HighestInterestFirstPayer
from .interestaccruer import InterestAccruer
from .loan import Loan
from .loaninfo import LoanInfo
from .loanreader import LoanReader
from .loanutils import total_owed_on_loans
from .minpayer import MinPaymentPayer
from .money import Money
from .process import Process 


def plot(x, y):
  fig, ax = plt.subplots(figsize=(4, 3), dpi=150)
  ax.plot(x, y / 1000, ls="-")
  ax.set_title('Total owed on student loans')
  ax.set_xlabel('days')
  ax.set_ylabel('Money (1000 USD)')
  plt.tight_layout()
  plt.show()


class Finance:

  def __init__(self, options):
    self.options = options
    self.process = Process()

  def loan_datum_to_loan(self, datum):
    """Convert loanreader's data into Loan instances"""
    balance = Money(datum['balance'])
    interest = float(datum['interest rate'])
    bill_day = datum['bill day']
    pay_day = datum['pay day']
    min_payment = float(datum['minimum payment'])
    if datum['status'] == 'in progress':
      bill_info = BillInfo(bill_day, min_payment)
      loan_info = LoanInfo(balance, interest)
    elif datum['status'] == 'forbearance':
      bill_info = BillInfo(bill_day, min_payment, False)
      loan_info = LoanInfo(balance, interest, False)
    elif datum['status'] == 'deferred':
      bill_info = BillInfo(bill_day, min_payment, False)
      loan_info = LoanInfo(balance, interest)
    else:
      raise Exception(f"Invalid loan status in CSV file: {datum['status']}")
    
    try:
      result = Loan(loan_info, bill_info)
    except:
      raise

    return result

  def run(self):
    """
    """
    account = Account(Money(1000000.00))

    loan_reader = LoanReader('etc/loans.csv')
    # loan_reader = LoanReader('etc/example_loans.csv')
    loan_data = loan_reader.read() # \todo need something to validate the data
    
    loans = []
    for datum in loan_data:
      loans.append(self.loan_datum_to_loan(datum))

    total = total_owed_on_loans(loans)
    print(f'Total balance {total}')

    # End date will trump num_days
    num_days = self.options.known.num_days
    today = datetime.date.today()
    if self.options.known.end_date:
      end_date = datetime.datetime.strptime(self.options.known.end_date, '%b %d %Y')
      num_days = (end_date - today).days

    days = np.arange(0, num_days, 1)
    totals = np.zeros(len(days))
    
    current_date = DateSubject(today)

    min_pay_loans = []
    for l in loans:
      min_pay_loans.append(MinPaymentPayer(l, account))

    for l in min_pay_loans:
      current_date.register(l)

    interest_accruers = []
    for l in loans:
      interest_accruers.append(InterestAccruer(l))

    for l in interest_accruers:
      current_date.register(l)


    # high_interest_payer = HighestInterestFirstPayer(loans, account, 1, Money(2000.00))
    # current_date.register(high_interest_payer)

    for day in range(num_days):

    #   # high_interest_payer = HighestInterestFirstPayer(loans, account, 1, Money(2000.00))
    #   # current_date.register(high_interest_payer)

      current_date.increment_day()

    #   # obs_loans = [l for l in obs_loans if l.total_owed != Money()]
    #   # loans = [l for l in loans if l.total_owed != Money()]
      
    #   # current_date.unregister(high_interest_payer)

      totals[day] = float(total_owed_on_loans(loans))

    if not self.options.known.disable_figure:
      proc = multiprocessing.Process(target=plot, args=(days, totals))
      proc.start()

    print(f'Total balance {total_owed_on_loans(loans)}')
