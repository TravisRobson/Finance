

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
  data = yaml.load(file, Loader=yaml.FullLoader)

  loan_data = data.get('loans', None)
  payer_data = data.get('payers', None)

  return loan_data, payer_data
