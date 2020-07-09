#!/usr/bin/env python3


import sys
from logging import basicConfig, getLogger, DEBUG
import yaml

from finance import Finance
from finance import Options


def main(args):
  """
  Finance executable
  """
  print('Welcome to Finance')

  logger = getLogger(__name__)

  options = Options()
  options.parse(args[1:])

  basicConfig(filename='finance.log', level=DEBUG)

  finance = Finance(options)

  finance.run()


if __name__ == '__main__':

  main(sys.argv)