#!/usr/bin/env python3


from decimal import Decimal
from unittest import TestCase

from finance.src.money import Money


def test_from_string():
  money = Money.from_string("10.00")
  assert money.amount == Decimal("10.00")


class MoneyTestCase(TestCase):
  
  def test_create(self):
    
