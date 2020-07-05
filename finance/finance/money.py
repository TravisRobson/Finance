#!/usr/bin/env python3


from random import uniform
import pytest

from decimal import Decimal, ROUND_HALF_UP


def almost_equal(a, b):
  assert isinstance(a, Money)
  assert isinstance(b, Money)
  return abs(a - b) < 1.0e-3
  

class Money:

  def __init__(self, amount=None):
    if isinstance(amount, Decimal):
      self._amount = amount or Decimal(0)
    else:
      self._amount = Decimal(amount or 0)

  @classmethod
  def from_string(cls, amount):
    return Money(Decimal(amount))

  @property
  def amount(self):
    return self._amount

  def __str__(self):
    return f"${self._amount:.2f}"

  def __repr__(self):
    return f"{self._amount}"

  def __float__(self):
    return float(self._amount)

  def __add__(self, rhs):
    if isinstance(rhs, Money):
      return Money(amount = self._amount + rhs.amount)
    else:
      return Money(amount = self._amount + Decimal(rhs))
   
  def __sub__(self, rhs):
    if isinstance(rhs, Money):
      return Money(amount = self._amount - rhs.amount)
    else:
      return Money(amount = self._amount - Decimal(rhs))

  def __pos__(self):
    return Money(amount = self._amount)

  def __neg__(self):
    return Money(amount = -self._amount)

  def __abs__(self):
    return Money(amount = abs(self._amount))

  def __round__(self, n=2):
    """todo Is this how I wish to round things?"""
    rounded_amount = self._amount.quantize(Decimal('0.01'), ROUND_HALF_UP)
    return Money(amount = rounded_amount)

  def __mul__(self, rhs):
    return Money(amount = Decimal(rhs) * self._amount)

  def __truediv__(self, rhs):
    return Money(amount = self._amount / Decimal(rhs))

  __radd__ = __add__ # commutative
  __rmul__ = __mul__ # commutative

  def __lt__(self, rhs):
    if isinstance(rhs, Money):
      return self._amount < rhs._amount
    else:
      return self < Money(rhs)

  def __le__(self, rhs):
    if isinstance(rhs, Money):
      return self._amount <= rhs._amount
    else:
      return self <= Money(rhs)   

  def __gt__(self, rhs):
    if isinstance(rhs, Money):
      return self._amount > rhs._amount
    else:
      return self > Money(rhs)

  def __ge__(self, rhs):
    if isinstance(rhs, Money):
      return self._amount >= rhs._amount
    else:
      return self >= Money(rhs)

  def __eq__(self, rhs):
    if isinstance(rhs, Money):
      return self._amount == rhs._amount
    else:
      return self == Money(rhs)

  def __bool__(self):
    return round(self._amount, 2) != 0

  __nonzero__ = __bool__





