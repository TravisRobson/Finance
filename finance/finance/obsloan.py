#!/usr/bin/env python3


import abc
import datetime


class Observer(abc.ABC):

  @abc.abstractmethod
  def update(self, subject) -> None:
    pass


class ObserverLoan(Observer):

  def __init__(self, loan):
    self._loan = loan

  def update(self, subject):
    tt = subject.date.timetuple()
    bill_date = datetime.date(tt.tm_year, tt.tm_mon, self._loan.bill_day) 
    self._loan.accrue_daily(tt.tm_year)
    if bill_date == subject.date:
      self._loan.convert_accrued_to_principal()
      