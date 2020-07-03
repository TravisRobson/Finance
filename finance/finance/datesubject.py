#!/usr/bin/env python3


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


class DateSubject(Subject):

  def __init__(self, date):
    
    self._date = date
    self._observers = []

  @property
  def date(self):
    return self._date

  def increment_day(self):
    self._date += datetime.timedelta(days=1)
    self.notify()
  
  def register(self, observer) -> None:
    self._observers.append(observer)

  def unregister(self, observer) -> None:
    self._observers.remove(observer)

  def notify(self) -> None:
    for obs in self._observers:
      obs.update(self)
