#!/usr/bin/env python3

import datetime
import multiprocessing

import numpy as np


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
from .moneydateplot import money_date_plot
from .money import Money
from .process import Process 


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
    initial_amount = Money(1000000.00)
    account = Account(initial_amount)

    payment_per_month = 2118.79 # my rough monthly amount

    loan_reader = LoanReader('etc/loans.csv')
    # loan_reader = LoanReader('etc/example_loans.csv')
    loan_data = loan_reader.read() # \todo need something to validate the data
    
    loans = []
    for datum in loan_data:
      loans.append(self.loan_datum_to_loan(datum))

    total = total_owed_on_loans(loans)
    print(f'Initial total balance {total}')

    # End date will trump num_days
    num_days = self.options.known.num_days
    today = datetime.date.today()
    if self.options.known.end_date:
      end_date = datetime.datetime.strptime(self.options.known.end_date, '%b %d %Y')
      num_days = (end_date - today).days

    days = np.arange(0, num_days + 1, 1)
    totals = np.array([])

    dates = []
    dates.append(today)
    totals = np.append(totals, float(total_owed_on_loans(loans)))
    
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

    high_interest_payer = HighestInterestFirstPayer(loans, account, 1, Money(2000.00))
    current_date.register(high_interest_payer)

    for day in range(1,num_days+1):

      current_date.increment_day()
      dates.append(current_date.date)

      totals = np.append(totals, float(total_owed_on_loans(loans)))

      if total_owed_on_loans(loans) == Money(0.00):
        break

    if not self.options.known.disable_figure:
      proc = multiprocessing.Process(target=money_date_plot, args=(dates, totals))
      proc.start()

    print(f'Ending total balance {total_owed_on_loans(loans)}')
    total_days = (dates[-1] - today).days
    print(f'Last day: {dates[-1]}, total days: {total_days}, i.e. ~{total_days/365.:.2f} years')
    print(f'Amount paid: {initial_amount-account.balance}')
