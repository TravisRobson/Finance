#!/usr/bin/env python3


import csv


class LoanReader:
  """Read a CSV formatted file storing loan data"""
  def __init__(self, filename):
    self._loans = []
    self._filename = filename



  def read(self):

    # \todo need some error checking here for an invalid file
    with open(self._filename, 'rt') as file:
      reader = csv.DictReader(file) 

      for row in reader:
        print(row)
        self._loans.append(row)

    return self._loans





