

from .exceptions import FinanceError

import yaml

class ParserError(FinanceError):

  def __init__(self, key):
    super(ParserError, self).__init__("YAML data file expected key: {key}")
    self._key = key


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


def get_start_date(data):
  return data.get('date modified', None)


def get_account_data(data):
  """Currently singular"""
  return data.get('account', None)


def get_payers_data(data):
  return data.get('payers', None)
