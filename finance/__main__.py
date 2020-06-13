#!/usr/bin/env python3


import sys

from src import Options


def main(args):
  """Finance executable"""
  print('Welcome to Finance')

  processor = CmdLineProcessor()
  processor.parse(args[1:])


if __name__ == '__main__':

  main(sys.argv)