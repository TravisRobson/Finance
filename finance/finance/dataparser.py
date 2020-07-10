

from .exceptions import FinanceError

import yaml


class ParserError(FinanceError, KeyError):
  """If there is an error while parsing"""
  def __init__(self, key):
    super(FinanceError, self).__init__(f'Expected YAML list: {key}')
    self.key = key
    

def parse(file):

  data = yaml.load(file, Loader=yaml.FullLoader)

  try:
    loan_data = data['loans']
  except KeyError as err:
    raise ParserError('loans')

  return loan_data
