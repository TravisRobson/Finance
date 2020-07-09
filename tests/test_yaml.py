

from finance.finance.billinfo import BillInfo
import yaml


def test_dummy():


  with open('etc/finance_example.yaml') as file:
    data = yaml.load(file, Loader=yaml.FullLoader)

  print(data)

  assert False