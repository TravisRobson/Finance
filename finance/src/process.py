#!/usr/bin/env
"""

"""

import subprocess


class Process:

  def __init__(self):
    pass

  def run(self, command):
    result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    out, err = result.communicate() # wait until process completes
    # \todo should probably log these?
    if result.returncode:
      raise ProcessException(result.returncode)

    return out


class ProcessException(Exception):

  def __init__(self, returncode):
    self.returncode = returncode

  def __str__(self):
    return repr(self.returncode)