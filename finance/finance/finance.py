

import datetime
import multiprocessing

import numpy as np

from .account import Account
from .datesubject import DateSubject
from .highinterestpayer import HighestInterestFirstPayer
from .interestaccruer import InterestAccruer
from .loanutils import total_owed_on_loans
from .loanprocessor import LoanProcessor
from .minpayer import MinPaymentPayer
from .moneydateplot import money_date_plot
from .money import Money
from .startaccruing import StartAccruingObserver
from .startbilling import StartBillingObserver

import finance.account as account
import finance.dataparser as parser
import finance.exceptions as exceptions
import finance.loan as loan


class Finance:
  
  MAX_ITERATIONS = 365 * 80 # 80 years is a suffient upper bound

  def __init__(self, options):
    self._options = options
    self._today = datetime.date.today()
    self._dates = [] # dates of the simulation
    self._totals = np.array([]) # float balance for all loans
    self._loans = []
    self._counter = 0 # make sure we don't enter an infinte loop

  def _display_results(self, dates, totals):
    """
    Display the figure of cumulative loan balance and some summary stats
    as text to screen.
    """
    if not self._options.disable_figure:
      proc = multiprocessing.Process(target=money_date_plot, args=(dates, totals))
      proc.start()

    print(f'Ending total balance {total_owed_on_loans(self._loans)}')
    total_days = (dates[-1] - self._today).days
    print(f'Last day: {dates[-1]}, total days: {total_days}, i.e. ~{total_days / 365.:.2f} years')
    print(f'Amount paid: {self._init_amount - self._account.balance}')

  def _calc_total_min_payments(self):
    """Total minimum payments for all loans that are collection payments"""
    total_min_payment = Money(0.00)
    for l in self._loans:
      if l.bill_in_progress and l.total_owed > Money(0.00):
        total_min_payment += l.min_payment 
        
    return total_min_payment  

  def _create_observers(self, date_subject):
    """
    Create various observers of the date to synchonize 
    billing and loan interest accruing.
    """
    for l in self._loans:
      date_subject.register(InterestAccruer(l)) # interest accrues before payment is made
      date_subject.register(MinPaymentPayer(l, self._account))

      if not l.bill_in_progress:
        date_subject.register(StartBillingObserver(l))

      if not l.accruing:
        date_subject.register(StartAccruingObserver(l))

  def _read_loans_data(self, data):
    loan_data = parser.get_loans_data(data)
    self._loans = loan.create_loans(loan_data)
    print(f'Initial total balance {total_owed_on_loans(self._loans)}')

  def _read_start_date_data(self, data):
    self._start_date = datetime.datetime.strptime(parser.get_start_date(data), "%m-%d-%Y").date()
    print(f'Starting date: {self._start_date}')

  def _read_account_data(self, data):
    account_data = parser.get_account_data(data)
    self._account = account.create_account(account_data)
    self._init_amount = self._account.balance
    print(f'Initial account balance: {self._init_amount}')

  def _read_data_file(self):
    with open('etc/finance.yaml') as file:
      data = parser.parse(file)

      self._read_loans_data(data)
      self._read_start_date_data(data)
      self._read_account_data(data)

      #monthly_pay  = self._options.monthly_pay or parser.get_loans_monthly_payment(data)
      # self._payment_per_month = Money(monthly_pay) 

  def initialize(self):
    self._read_data_file()

  def _stop(self, date):
    """
    There are three options to stop the update loop:
      1) Loans have all been killed
      2) Date has reached user-specified end date
      3) Number of days iterated over has reached user-specified amount
    """
    self._counter += 1
    if self._counter > Finance.MAX_ITERATIONS:
      raise exceptions.FinanceError(f"Exceeded maximum iterations. counter: {self._counter}, max: {Finance.MAX_ITERATIONS}")

    result = False
    if not self._options.end_date and not self._options.num_days:
      result = total_owed_on_loans(self._loans) <= Money(0.00)
    elif self._options.num_days:
      result = (date - self._start_date).days >= self._options.num_days
    else:
      result = date >= self._options.end_date

    return result

  def run(self):
    dates = [self._start_date]
    totals = np.array([float(total_owed_on_loans(self._loans))])

    date_subject = DateSubject(self._start_date) # the date of the update loop

    while not self._stop(date_subject.date):
      date_subject.increment_day()

      dates.append(date_subject.date)
      totals = np.append(totals, float(total_owed_on_loans(self._loans)))

    self._display_results(dates, totals)

    # # End date will trump num_days
    # num_days = self._options.num_days

    # if self._options.end_date:
    #   end_date = datetime.datetime.strptime(self._options.end_date, '%b %d %Y')
    #   num_days = (end_date - self._today).days

    # days = np.arange(0, num_days + 1, 1)

    # self._dates.append(self._today)
    # self._totals = np.append(self._totals, float(total_owed_on_loans(self._loans)))
    
    # current_date = DateSubject(self._today)
    # self._create_observers(current_date)

    # high_interest_payment = payment_per_month - self._calc_total_min_payments()
    # print(f"Initial total monthly min payments: {self._calc_total_min_payments()}")

    # high_interest_payer = HighestInterestFirstPayer(self._loans, self._account, 1, high_interest_payment)
    # current_date.register(high_interest_payer)

    # for day in range(1,num_days+1):

    #   current_date.increment_day()
    #   self._dates.append(current_date.date)

    #   # If more loans start to be billed, adjust amount paying on highest interest
    #   high_interest_payer.amount = payment_per_month - self._calc_total_min_payments()

    #   self._totals = np.append(self._totals, float(total_owed_on_loans(self._loans)))

    #   if total_owed_on_loans(self._loans) == Money(0.00):
    #     break

    # self._display_results()

