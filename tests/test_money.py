#!/usr/bin/env python3


from decimal import Decimal
from unittest import TestCase

from finance.finance.money import Money


class MoneyTestCase(TestCase):

  def test_create_from_float(self):
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


  def test_add(self):
    a = Money(1.30)
    b = Money(2.60)
    self.assertAlmostEqual(a + b, Money(3.90))


  def test_sub(self):
    a = Money(3.45)
    b = Money(4.60)
    self.assertAlmostEqual(a - b, Money(-1.15))


  def test_neg(self):
    self.assertAlmostEqual(-Money(3.67), Money(-3.67))


  def test_abs(self):
    self.assertAlmostEqual(Money(1.23), abs(Money(-1.23)))


  def test_mul(self):
    a = Money(3.33)
    b = 4 * a
    self.assertAlmostEqual(b, Money(13.32))


  def test_div(self):
    a = Money(3.33)
    b = a / 3
    self.assertAlmostEqual(b, Money(1.11))


  def test_lt(self):
    one = Money(1)
    two = Money(2)
    self.assertTrue(one < two)


  def test_gt(self):
    one = Money(1)
    two = Money(2)
    self.assertTrue(two > one)


  def test_eq(self):
    a = Money(1.45)
    b = Money(1.45)
    self.assertEqual(a, b)


  def test_bool_true(self):
    self.assertTrue(Money(1))


  def test_bool_false(self):
    self.assertFalse(Money(0))












