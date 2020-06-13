#!/usr/bin/env python3


import sys

from src import Options
from src import Finance


def main(args):
  """Finance executable"""
  print('Welcome to Finance')

  options = Options()
  options.parse(args[1:])

  finance = Finance(options)

  print(f"CSV files: {finance.list_csv_files()}")


if __name__ == '__main__':

  main(sys.argv)