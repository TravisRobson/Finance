#!/usr/bin/env python3


from decimal import Decimal


class Money:

  def __init__(self, amount=None):
    if isinstance(amount, Decimal):
      self._amount = amount
    else:
      self._amount = Decimal(amount or 0)


  @property
  def amount(self):
    return self._amount


  def __str__(self):
    return f"{self._amount}"


  def __repr__(self):
    return str(self)

    
  def __add__(self, rhs):
    return Money(amount=self._amount + rhs.amount)
