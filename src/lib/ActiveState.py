# ----------------------------------------------------------------------------
# ActiveState.py: Handle active-state, i.e. display current values
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
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
    if self._app.display:
      self._values   = [ValuesView(app.display,app.border,
                              app.data_provider.get_units()),
                        ValuesView(app.display,app.border,['s','s'])] # elapsed
                      

  # --- write settings to serial   -------------------------------------------

  def _log_settings(self):
    """ write settings """

    print("\n#Interval: {0:d}ms".format(self._settings.interval))
    print("#Duration:   {0:d}s".format(self._settings.duration))
    print("#Update:     {0:d}ms\n".format(self._settings.update))

  # --- loop during ready-state   --------------------------------------------

  def run(self):
    """ main-loop during active-state """

    self._log_settings()

    # first level:  aggregate raw-data    -> sample-data (mean)
    # second level: aggregate sample-data -> measurement-data (min,mean,max)
    #               aggregate sample-data -> display-data (mean)
    dim = self._app.data_provider.get_dim()
    s_data = DataAggregator(dim)
    m_data = DataAggregator(dim)
    if self._app.display:
      c_view = 0
      d_data = DataAggregator(dim)

    # reset data-provider and wait for first sample
    self._app.data_provider.reset()
    self._app.data_provider.get_data()

    if self._settings.duration:
      end = time.monotonic() + self._settings.duration
    else:
      end = sys.maxsize

    stop = False
    start_t = time.monotonic()                        # for final stats
    while not stop and time.monotonic() < end:
      if self._app.display:
        # reset display-data
        d_data.reset()
        display_next = time.monotonic() + self._settings.update/1000
      else:
        display_next = sys.maxsize

      # sample data while in update-interval
      while not stop and time.monotonic() < display_next:
        # reset sample-data
        s_data.reset()
        sample_next = time.monotonic() + self._settings.interval/1000

        # sample data while in sample-interval
        while not stop and time.monotonic() < sample_next:
          if self._app.key_events:
            key = self._app.key_events.is_key_pressed(
              self._app.key_events.KEYMAP_ACTIVE)
            if key == 'TOGGLE' and self._app.display:
              # switch to next view
              c_view = (c_view+1) % len(self._values)
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
        if self._app.display:
          d_data.add(mean)

      if stop:
        break

      if self._app.display:
        # time to update the display
        if c_view == 0:
          # measurement values
          mean = d_data.get_mean()
          self._values[c_view].set_values(mean,time.monotonic()-start_t)
        elif c_view == 1:
          # elapsed time
          self._values[c_view].set_values([time.monotonic()-start_t,
                                           self._settings.duration],-1)
        self._values[c_view].show()
        if not self._app.key_events:
          # auto toggle view
          c_view = (c_view+1) % len(self._values)

    # that's it, save and log results
    self._app.results.time   = time.monotonic() - start_t
    self._app.results.values = m_data.get()

    print("\n#Duration: {0:.1f}s".format(self._app.results.time))
    print("#Min,Mean,Max")
    units = self._app.data_provider.get_units()
    for index,value in enumerate(self._app.results.values):
      print("#{1:.2f}{0:s},{2:.2f}{0:s},{3:.2f}{0:s}".format(units[index],*value))
