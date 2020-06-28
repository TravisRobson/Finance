#!/usr/bin/env python3


import pytest

from finance.finance.loan import Loan


import abc
import datetime

class Subject(abc.ABC):
  """Subject interface, contains functions to manage subscribers"""
  @abc.abstractmethod
  def register(self, observer) -> None:
    pass

  @abc.abstractmethod
  def unregister(self, observer) -> None:
    pass

  @abc.abstractmethod
  def notify(self) -> None:
    """Notify observers about an event"""
    pass


class DatetimeSubject(Subject):

  def __init__(self, date):
    self._date = date
    self._observers = []

  @property
  def date(self):
    return self._date


  def increment_day(self):
    self._date += datetime.timedelta(days=1)
  

  def register(self, observer) -> None:
    self._observers.append(observer)

  def unregister(self, observer) -> None:
    self._observers.remove(observer)

  def notify(self) -> None:
    for obs in self._observers:
      obs.update(self)


class Observer(abc.ABC):

  @abc.abstractmethod
  def update(self, subject) -> None:
    pass


class LoanStepper(Observer):

  def __init__(self, loan):
    self._loan = loan

  def update(self, subject):
    tt = subject.date.timetuple()
    bill_date = datetime.date(tt.tm_year, tt.tm_mon, self._loan.bill_day_of_month) 
    if bill_date == subject.date:
      print('PAY')
    else:
      print("You're free")


def test_foo():
  date = datetime.date(2020, 6, 26)
  working_date = DatetimeSubject(date)


  loan = Loan(100.00, 1.0, 27, 15)
  loan_stepper = LoanStepper(loan)

  loan_stepper.update(working_date)

  working_date.increment_day()
  loan_stepper.update(working_date)
  assert False


