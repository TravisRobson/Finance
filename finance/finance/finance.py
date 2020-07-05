

import datetime
import multiprocessing

import numpy as np

from .account import Account
from .datesubject import DateSubject
from .highinterestpayer import HighestInterestFirstPayer
from .interestaccruer import InterestAccruer
from .loanutils import total_owed_on_loans
from .loanprocessor import LoanProcessor
from .startbilling import StartBillingObserver
from .startaccruing import StartAccruingObserver
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

  def _calc_total_min_payments(self):
    total_min_payment = Money(0.00)
    for l in self._loans:
      if l.bill_in_progress and l.total_owed > Money(0.00):
        total_min_payment += l.min_payment 
        
    return total_min_payment  

  def _create_observers(self, date_subject):
    """
    Create various observers of the date to synchonize 
    billing, and loan interest accruing.
    """
    for l in self._loans:
      date_subject.register(InterestAccruer(l)) # interest accrues before payment is made
      date_subject.register(MinPaymentPayer(l, self._account))
      #date_subject.register(InterestAccruer(l)) # interest accrues before payment is made


      if not l.bill_in_progress:
        date_subject.register(StartBillingObserver(l))

      if not l.accruing:
        date_subject.register(StartAccruingObserver(l))

  def run(self):
    payment_per_month = Money(self._options.monthly_pay) # my rough monthly amount

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
    self._create_observers(current_date)

    high_interest_payment = payment_per_month - self._calc_total_min_payments()
    print(f"Initial total monthly min payments: {self._calc_total_min_payments()}")

    high_interest_payer = HighestInterestFirstPayer(self._loans, self._account, 1, high_interest_payment)
    current_date.register(high_interest_payer)

    for day in range(1,num_days+1):

      current_date.increment_day()
      self._dates.append(current_date.date)

      # If more loans start to be billed, adjust amount paying on highest interest
      high_interest_payer.amount = payment_per_month - self._calc_total_min_payments()

      self._totals = np.append(self._totals, float(total_owed_on_loans(self._loans)))

      if total_owed_on_loans(self._loans) == Money(0.00):
        break

    self._display_results()

