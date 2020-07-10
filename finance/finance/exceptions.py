

class FinanceError(Exception):
  """All exceptions raise from my code will inherit from this"""
  def __init__(self, msg=None):
    if msg is None:
      msg = "An error occured in the Finance code"
      super(FinanceError, self).__int__(msg)
      

class InvalidBillDayOfMonth(Exception):

  def __init__(self, value):
    self._value = value

  def __str__(self):
    return f"value ({self._value})"

  @staticmethod
  def is_valid(day):
    if not 1 <= int(day) <= 28:
      return False
    return True