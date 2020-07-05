

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def money_date_plot(dates, money):
  fig, ax = plt.subplots(figsize=(4, 3), dpi=150)

  ax.plot(dates, money / 1000, ls="-")
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%b, %y'))
  ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))

  ax.set_title('Total owed on student loans')
  ax.set_xlabel('date')
  ax.set_ylabel('Money (1000 USD)')
  plt.gcf().autofmt_xdate()
  plt.tight_layout()
  plt.show()