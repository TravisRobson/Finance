#!/usr/bin/env python3


from .money import Money


def total_owed_on_loans(loan_list):
  total = Money()
  for loan in loan_list:
    total += loan.total_owed

  return total
