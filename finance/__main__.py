#!/usr/bin/env python3


import sys

from src import Options
from src import Finance
from src import LoanReader

def main(args):
  """Finance executable"""
  print('Welcome to Finance')

  options = Options()
  options.parse(args[1:])

  finance = Finance(options)

  print(f"CSV files: {finance.list_csv_files()}")

  loan_reader = LoanReader('etc/loans.csv')

  loan_data = loan_reader.read()

  # \todo need something to validate the data

  total = 0.0
  for loan in loan_data:
    for key, value in loan.items():
      if key.strip() == 'balance':
        total += float(value)

  print(f'Total balance ${total}')


if __name__ == '__main__':

  main(sys.argv)