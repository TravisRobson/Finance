#!/usr/bin/env python3


from decimal import Decimal
from unittest import TestCase

from finance.finance.money import Money


class MoneyTestCase(TestCase):

  def test_create_from_int_literal(self):
    """
    For user's convenience we expect to be able to construct a Money instance
    from a float or int.
    """
    result = Money(10)
    self.assertEqual(result.amount, 10)

    result = Money(-10)
    self.assertEqual(result.amount, -10)

    result = Money(1.23)
    self.assertEqual(result.amount, 1.23)


  def test_create_from_string(self):
    """
    For user's convenience we wish to be able to construct a Money instance
    from a string.
    """
    result = Money.from_string("10.00")
    self.assertEqual(result.amount, Decimal("10.00"))

    result = Money.from_string("-15.34")
    self.assertEqual(result.amount, Decimal("-15.34"))


  def test_less_than(self):
    one = Money(1)
    two = Money(2)
    self.assertTrue(one < two)

