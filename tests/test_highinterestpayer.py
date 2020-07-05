

import copy
import datetime

import pytest

from finance.finance.account import Account
from finance.finance.billinfo import BillInfo
from finance.finance.datesubject import DateSubject
from finance.finance.highinterestpayer import HighestInterestFirstPayer
from finance.finance.loan import Loan
from finance.finance.loaninfo import LoanInfo
from finance.finance.money import Money


def next_day(date):
  return (date + datetime.timedelta(days=1)).day


@pytest.fixture
def current_date():
  """Create date subject for loan to watch."""
  date = datetime.date(2020, 7, 4)
  return DateSubject(date)


def test_nonzero_balance_loan(current_date):
  """
  If there is a nonzero balance loan total owed of highinterestpayer
  should change, and account amount should change.
  """
  init_account_balance = Money(10000.00)
  account = Account(init_account_balance)

  bill_info = BillInfo(day=10, amount=Money(1.00)) 
  loan_info = LoanInfo(Money(100.00), interest=1.00)

  loans = [Loan(loan_info, bill_info)]

  payer = HighestInterestFirstPayer(loans, account, 8, Money(10.00))
  init_total_owed = payer.total_owed

  current_date.register(payer)
  for i in range(31):
    current_date.increment_day()

  assert init_account_balance != account.balance
  assert init_total_owed != payer.total_owed


def test_account_loan_balance_adjusts(current_date):
  """
  The total_owed on a loan and change in account balance should 
  be changed in a specific way.
  """
  init_account_balance = Money(10000.00)
  account = Account(init_account_balance)

  init_loan_balance = Money(100.00)
  bill_info = BillInfo(day=10, amount=Money(1.00)) # days after dates covered in this test
  loan_info = LoanInfo(init_loan_balance, interest=1.00)

  loans = [Loan(loan_info, bill_info)]

  # pay day after current_date (5)
  pay_amount = Money(10.00)
  payer = HighestInterestFirstPayer(loans, account, next_day(current_date.date), pay_amount)
  init_total_owed = payer.total_owed

  current_date.register(payer)
  current_date.increment_day()

  assert account.balance + pay_amount == init_account_balance
  assert loans[0].total_owed + pay_amount == init_loan_balance


def test_dont_overpay_small_balance_loan(current_date):
  """
  If a loan has only a small balance left, and the
  HighestInterestFirstPayer's amount is greater than that balance
  do not overpay.
  """
  init_account_balance = Money(10000.00)
  account = Account(init_account_balance)

  init_loan_balance = Money(100.00)
  bill_info = BillInfo(day=10, amount=Money(1.00)) # days after dates covered in this test
  loan_info = LoanInfo(init_loan_balance, interest=1.00)

  loans = [Loan(loan_info, bill_info)]

  # pay day after current_date (5)
  pay_amount = Money(200.00)
  payer = HighestInterestFirstPayer(loans, account, next_day(current_date.date), pay_amount)
  init_total_owed = payer.total_owed

  current_date.register(payer)
  current_date.increment_day()

  assert account.balance + init_loan_balance == init_account_balance
  assert loans[0].total_owed == Money(0.00)


def test_highest_interest_first(current_date):
  """
  If there are 2+ loans, the loan with highest interest 
  receives the payment.
  """
  init_account_balance = Money(10000.00)
  account = Account(init_account_balance)

  init_loans = []
  init_loan_balance = Money(100.00)
  bill_info = BillInfo(day=10, amount=Money(1.00)) # days after dates covered in this test
  loan_info = LoanInfo(init_loan_balance, interest=1.00)  
  init_loans.append(Loan(loan_info, bill_info))

  loan_info = LoanInfo(init_loan_balance, interest=loan_info.interest + 1.00)  
  init_loans.append(Loan(loan_info, bill_info))

  loans = copy.deepcopy(init_loans)

  payer = HighestInterestFirstPayer(loans, account, next_day(current_date.date), Money(100.00))

  current_date.register(payer)
  current_date.increment_day() 

  # second loan, the higher interest one, should have a different balance
  assert init_loans[1].balance != loans[1].balance

  # but lower interest one should be unchanged in this test
  assert init_loans[0].balance == loans[0].balance


def test_multiple_loans_highest_interest_first(current_date):
  """
  If there are 2+ loans, where payer's amount covers at least one of the
  loan's remaining balance, and then some, the second highest interest
  loan is the loan whose balance gets paid down.
  """
  init_account_balance = Money(10000.00)
  account = Account(init_account_balance)

  init_loans = []
  init_loan_balance = Money(100.00)
  bill_info = BillInfo(day=10, amount=Money(1.00)) # days after dates covered in this test
  loan_info = LoanInfo(init_loan_balance, interest=1.00)  
  init_loans.append(Loan(loan_info, bill_info))

  loan_info = LoanInfo(init_loan_balance, interest=loan_info.interest + 1.00)  
  init_loans.append(Loan(loan_info, bill_info))

  loan_info = LoanInfo(init_loan_balance, interest=loan_info.interest - 0.50)  
  init_loans.append(Loan(loan_info, bill_info))  

  loans = copy.deepcopy(init_loans)

  payer = HighestInterestFirstPayer(loans, account, next_day(current_date.date), init_loan_balance + Money(50.00))

  current_date.register(payer)
  current_date.increment_day() 

  # first loan in this test should remain unchanged.
  assert loans[0].balance == init_loans[0].balance

  # Second loan should have zero money left
  assert loans[1].balance == Money(0.00)

  # Third loan should have a reduced balance
  assert loans[2].balance == init_loans[2].balance - Money(50.00)


def test_highest_interest_accruing(current_date):
  """
  If there are multiple loans, it's the highest interest loans who
  are accruing that are addressed first.
  """
  init_account_balance = Money(10000.00)
  account = Account(init_account_balance)

  init_loans = []
  init_loan_balance = Money(100.00)
  bill_info = BillInfo(day=10, amount=Money(1.00)) # days after dates covered in this test
  loan_info = LoanInfo(init_loan_balance, interest=1.00, accruing=False)  
  init_loans.append(Loan(loan_info, bill_info))

  loan_info = LoanInfo(init_loan_balance, interest=1.00)  
  init_loans.append(Loan(loan_info, bill_info)) 

  loans = copy.deepcopy(init_loans)

  payer = HighestInterestFirstPayer(loans, account, next_day(current_date.date), Money(50.00))

  current_date.register(payer)
  current_date.increment_day() 

  # first loan, nonaccruing, should not have a changed balance   
  assert loans[0].balance == init_loans[0].balance

  # second loan should have a decreased balance
  assert loans[1].balance + Money(50.00) == init_loans[1].balance
