# ----------------------------------------------------------------------------
# ActiveState.py: Handle active-state, i.e. display current values
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pico-cp-vameter
#
# ----------------------------------------------------------------------------

import time
import sys
from View import ValuesView
from Data import DataAggregator

class ActiveState:
  """ manage active-state """

  # --- constructor   --------------------------------------------------------

  def __init__(self,app):
    """ constructor """

    self._app      = app
    self._settings = app.settings
    self._fmt      = app.data_provider.get_fmt()
    self._results = app.results
    self._values = ValuesView(app.display,app.border)

  # --- loop during ready-state   --------------------------------------------

  def run(self):
    """ main-loop during active-state """

    # first level:  aggregate raw-data    -> sample-data (mean)
    # second level: aggregate sample-data -> measurement-data (min,mean,max)
    #               aggregate sample-data -> display-data (mean)
    dim = self._app.data_provider.get_dim()
    s_data = DataAggregator(dim)
    m_data = DataAggregator(dim)
    d_data = DataAggregator(dim)

    if self._settings.duration:
      end = time.monotonic() + self._settings.duration
    else:
      end = sys.maxsize

    stop = False
    while not stop and time.monotonic() < end:
      # reset display-data
      d_data.reset()
      display_next = time.monotonic() + self._settings.update

      # sample data while in update-interval
      while not stop and time.monotonic() < display_next:
        # reset sample-data
        s_data.reset()
        sample_next = time.monotonic() + self._settings.interval/1000

        # sample data while in sample-interval
        while not stop and time.monotonic() < sample_next:
          # TODO: check key-press
          try:
            sample = self._app.data_provider.get_data()
            s_data.add(sample)
          except StopIteration:
            stop = True
            break

        if stop:
          break

        # sampling finished: log data and add to aggregators
        _,mean,_ = s_data.get()
        print(self._fmt.format(1000*time.monotonic(),*mean))
        m_data.add(mean)
        d_data.add(mean)

      if stop:
        break

      # time to update the display
      _,mean,_ = d_data.get()
      self._values.set_values(*mean)
      self._values.show()

    # that's it, save results
    self._results.V = m_data.get(0)
    self._results.A = m_data.get(1)
