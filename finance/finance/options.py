#!/usr/bin/env python3
"""
brief--Command line options for the Finance application

author--Travis Robson
"""

from argparse import ArgumentParser


class Options:
  """Process the command line options"""
  def __init__(self):
    """Create parser and define command line arguments"""
    description = 'Execute the Finance application'
    self.parser = ArgumentParser(prog='finance', usage='./bin/%(prog)s [options]', description=description)

    self.parser.version = '0.1'

    self.parser.add_argument('-l', '--log-level', help='Application logging level')
    self.parser.add_argument('-s', '--save-figure', help='Save Matplotlib figures')


  def parse(self, args=None):
    """Parse known options, uknown options are ignored"""
    self.known, self.unknown = self.parser.parse_known_args(args)[:]

    if len(self.unknown) != 0:
      print(f'Warning, unknown arguments received {self.unknown}')