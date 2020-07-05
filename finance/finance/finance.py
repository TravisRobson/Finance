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
from .loanprocessor import LoanProcessor
from .minpayer import MinPaymentPayer
from .moneydateplot import money_date_plot
from .money import Money


class Finance:

  def __init__(self, options):
    self._options = options
    self._init_amount = Money(100000.00) # The initial amount of money person has "in the bank."
    self._account = Account(self._init_amount)
    self._today = datetime.date.today()
    self._dates = [] # dates of the simulation
    self._totals = np.array([]) # float balance for all loans
    self._loans = []

  def _display_results(self):
    """
    Display the figure of cumulative loan balance and some summary stats
    as text to screen.
    """
    if not self._options.disable_figure:
      proc = multiprocessing.Process(target=money_date_plot, args=(self._dates, self._totals))
      proc.start()

    print(f'Ending total balance {total_owed_on_loans(self._loans)}')
    total_days = (self._dates[-1] - self._today).days
    print(f'Last day: {self._dates[-1]}, total days: {total_days}, i.e. ~{total_days / 365.:.2f} years')
    print(f'Amount paid: {self._init_amount - self._account.balance}')

  def run(self):
    payment_per_month = 2118.79 # my rough monthly amount

    loan_processor = LoanProcessor('etc/loans.csv')
    self._loans = loan_processor.create_loans()    

    print(f'Initial total balance {total_owed_on_loans(self._loans)}')

    # End date will trump num_days
    num_days = self._options.num_days

    if self._options.end_date:
      end_date = datetime.datetime.strptime(self._options.end_date, '%b %d %Y')
      num_days = (end_date - self._today).days

    days = np.arange(0, num_days + 1, 1)

    self._dates.append(self._today)
    self._totals = np.append(self._totals, float(total_owed_on_loans(self._loans)))
    
    current_date = DateSubject(self._today)

    min_pay_loans = []
    for l in self._loans:
      min_pay_loans.append(MinPaymentPayer(l, self._account))

    for l in min_pay_loans:
      current_date.register(l)

    interest_accruers = []
    for l in self._loans:
      interest_accruers.append(InterestAccruer(l))

    for l in interest_accruers:
      current_date.register(l)

    high_interest_payer = HighestInterestFirstPayer(self._loans, self._account, 1, Money(2000.00))
    current_date.register(high_interest_payer)

    for day in range(1,num_days+1):

      current_date.increment_day()
      self._dates.append(current_date.date)

      self._totals = np.append(self._totals, float(total_owed_on_loans(self._loans)))

      if total_owed_on_loans(self._loans) == Money(0.00):
        break

    self._display_results()

