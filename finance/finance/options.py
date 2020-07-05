

from argparse import ArgumentParser


class Options:
  """Process the command line options"""
  def __init__(self):
    """Create parser and define command line arguments"""
    description = 'Execute the Finance application'
    self.parser = ArgumentParser(prog='finance', usage='./bin/%(prog)s [options]', description=description)

    self.parser.version = '0.1'

    self.parser.add_argument('-l', '--log-level', help='Application logging level')
    self.parser.add_argument('-n', '--num-days', type=int, default=300, help='Number of days to simulate')
    self.parser.add_argument('-e', '--end-date', type=str, default='', help='End date of simulation')
    self.parser.add_argument('-d', '--disable-figure', action='store_true', help='Do not display Matplotlib images')


  def parse(self, args=None):
    """Parse known options, uknown options are ignored"""
    self.known, self.unknown = self.parser.parse_known_args(args)[:]

    if len(self.unknown) != 0:
      print(f'Warning, unknown arguments received {self.unknown}')