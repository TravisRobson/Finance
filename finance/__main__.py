#!/usr/bin/env python3


import sys
import logging
import yaml

from finance import Finance
from finance import Options


def main(args):
  """
  Finance executable
  """
  print('Welcome to Finance')

  logger = logging.getLogger(__name__)

  options = Options()
  options.parse(args[1:])

  logging.basicConfig(filename='finance.log', level=logging.DEBUG)

  try:
    finance = Finance(options)
    finance.run()
  except Exception:
    logging.error("Failure in finance.run()", exc_info=True)


if __name__ == '__main__':

  main(sys.argv)