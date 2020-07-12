#!/usr/bin/env python3


import sys
import logging
import yaml

from finance.finance import Finance
from finance.options import Options


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

    finance.initialize()
    finance.run()
  except Exception as err:
    logging.error(f"Failure in finance.run(), exception: {err}", exc_info=True)
    raise err


if __name__ == '__main__':

  main(sys.argv)