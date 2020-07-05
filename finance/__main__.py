#!/usr/bin/env python3


import sys
from logging import basicConfig, getLogger, DEBUG
import yaml

from finance import Finance
from finance import Options
from finance import CliDefaults


def main(args):
  """
  Finance executable
  """
  print('Welcome to Finance')

  logger = getLogger(__name__)

  #########################################################
  # \todo need to migrate this elsewhere
  app_config_filename = "etc/finance.yaml"
  with open(app_config_filename, "r") as file:
    data = yaml.load_all(file, Loader=yaml.Loader)

    cli_defaults_found = False
    for d in data:
      if isinstance(d, CliDefaults):
        cli_defaults = d
        cli_defaults_found = True

  if not cli_defaults_found:
    raise Exception("CLI defaults not found in: {app_config_filename}")
  print(cli_defaults) 
  #########################################################

  options = Options(cli_defaults)
  options.parse(args[1:])

  basicConfig(filename='finance.log', level=DEBUG)

  finance = Finance(options)

  finance.run()


if __name__ == '__main__':

  main(sys.argv)