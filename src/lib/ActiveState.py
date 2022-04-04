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
    self._values = ValuesView(app.display,app.border,
                              app.data_provider.get_units())

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

    # reset data-provider and wait for first sample
    self._app.data_provider.reset()
    self._app.data_provider.get_data()

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
          key = self._app.key_events.is_key_pressed(
            self._app.key_events.KEYMAP_ACTIVE)
          if key == 'TOGGLE':
            # switch to plot-view
            pass
          elif key == 'STOP':
            stop = True
            break

          try:
            sample = self._app.data_provider.get_data()
            s_data.add(sample)
          except StopIteration:
            stop = True
            break

        if stop:
          break

        # sampling finished: log data and add to aggregators
        mean = s_data.get_mean()
        print(self._fmt.format(1000*time.monotonic(),*mean))
        m_data.add(mean)
        d_data.add(mean)

      if stop:
        break

      # time to update the display
      mean = d_data.get_mean()
      self._values.set_values(mean)
      self._values.show()

    # that's it, save results
    self._app.results = m_data.get()
