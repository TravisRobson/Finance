#!/usr/bin/env python3


import csv


class LoanReader:
  """Read a CSV formatted file storing loan data"""
  def __init__(self, filename):
    self._loans = []
    self._filename = filename

  def strip_keys(self):
    """Every element of the data that has extraneous white space, strip it"""
    for idx, loan in enumerate(self._loans):
      for key, val in loan.items():
        self._loans[idx][key] = self._loans[idx][key].strip() 

  def read(self):

    # \todo need some error checking here for an invalid file
    with open(self._filename, 'rt') as file:
      header = [h.strip() for h in file.readline().split(',')]
      reader = csv.DictReader(file, fieldnames=header) 

      for row in reader:
        self._loans.append(row)

    self.strip_keys()

    return self._loans





