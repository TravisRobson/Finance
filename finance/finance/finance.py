#!/usr/bin/env python3


from .process import Process # \todo need to figure out why I must prepend . to module names


class Finance:

  def __init__(self, options):
    self.options = options
    self.process = Process()

  def list_csv_files(self):
    return self._get_csv_files()

  def _get_csv_files(self):
    """
    List the *.csv files inside the etc/ folder

    Right now this is merely serving the purpose of an example for the 
    class that can run subprocesses
    """
    return self.process.run("ls etc/*.csv" ).decode('utf-8') 

  