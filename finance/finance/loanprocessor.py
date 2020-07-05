

from .loan import Loan


class LoanProcessor:
  """
  LoanReader class reads a text CSV file and creates a dictionary for each row.
  This class converts that data into a Loan instance.
  """
  def __init__(self, loan_dict):
    self._dict = loan_dict