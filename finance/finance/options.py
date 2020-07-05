

from argparse import ArgumentParser


class Options:
  """Process the command line options"""
  def __init__(self, cli_defaults):
    """Create parser and define command line arguments"""
    description = 'Execute the Finance application'
    self.parser = ArgumentParser(prog='finance', usage='./bin/%(prog)s [options]', description=description)

    self.parser.version = '0.1'

    self.parser.add_argument('-l', '--log-level', help='Application logging level')
    self.parser.add_argument('-n', '--num-days', type=int, default=cli_defaults.num_days, help='Number of days to simulate')
    self.parser.add_argument('-e', '--end-date', type=str, default='', help='End date of simulation')
    self.parser.add_argument('-d', '--disable-figure', action='store_true', help='Do not display Matplotlib images')
    self.parser.add_argument('-m', '--monthly-pay', type=float, default=cli_defaults.monthly_pay, help='Monthly payments on student loans')

  @property
  def num_days(self):
    return self._known.num_days
  
  @property
  def end_date(self):
    return self._known.end_date

  @property
  def disable_figure(self):
    return self._known.disable_figure
  
  @property
  def monthly_pay(self):
    return self._known.monthly_pay
  
  
  def parse(self, args=None):
    """Parse known options, uknown options are ignored"""
    self._known, self._unknown = self.parser.parse_known_args(args)[:]

    if len(self._unknown) != 0:
      print(f'Warning, unknown arguments received {self._unknown}')
