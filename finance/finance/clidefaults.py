

import yaml


class CliDefaults(yaml.YAMLObject):
  """
  Finance is a CLI application. The CLI has default values. To have 
  these collected all in one place, they have been migrated to the 
  Finance app's configuration file. This class stores the configurable
  parameters.
  """
  yaml_tag = u'!CliDefaults'
  def __init__(self, num_days, monthly_pay):
    self.num_days = num_days
    self.monthly_pay = monthly_pay

  def __repr__(self):
    msg = (
      f"{self.__class__.__name__}("
      f"num_days: {self.num_days}, "
      f"monthly_pay: {self.monthly_pay}"
      f")"
    )
    return msg
