

from .exceptions import FinanceError

import yaml


class ParserError(FinanceError, KeyError):
  """If there is an error while parsing"""
  def __init__(self, key):
    super(FinanceError, self).__init__(f'Expected YAML list: {key}')
    self.key = key


def parse(file):
  """
  Parse the data file (YAML format). Create dictionaries
  for each data type we could expect. If they don't exist
  return none.
  """
  return yaml.load(file, Loader=yaml.FullLoader)


def get_loans_data(data):
  """Get data needed to characterize loans"""
  return data.get('loans', None)


def get_payers_data(data):
  """Get data needed to characterize payment schemes"""
  return data.get('payers', None)


# def get_loans_monthly_payment(data):
#   return data.get('loans monthly payment', None)


def get_start_date(data):
  return data.get('date modified', None)


def get_account_data(data):
  """Currently singular"""
  return data.get('account', None)
