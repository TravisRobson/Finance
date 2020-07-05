

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