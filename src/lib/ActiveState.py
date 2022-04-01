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
import math
from View import ValuesView
from Data import DataAggregator

class ActiveState:
  """ manage active-state """

  # --- constructor   --------------------------------------------------------

  def __init__(self,app):
    """ constructor """

    self._app      = app
    self._settings = app.settings
    self._results = app.results
    self._values = ValuesView(app.display,app.border)

  # --- loop during ready-state   --------------------------------------------

  def run(self):
    """ main-loop during active-state """

    # first level:  aggregate raw-data    -> sample-data (mean)
    # second level: aggregate sample-data -> measurement-data (min,mean,max)
    #               aggregate sample-data -> display-data (mean)
    s_data = DataAggregator(2)
    m_data = DataAggregator(2)
    d_data = DataAggregator(2)

    if self._settings.duration:
      end = time.monotonic() + self._settings.duration
    else:
      end = 0

    while time.monotonic() < end:
      # reset display-data
      d_data.reset()
      display_next = time.monotonic() + self._settings.update

      # sample data while in update-interval
      while time.monotonic() < display_next:
        # reset sample-data
        s_data.reset()
        sample_next = time.monotonic() + self._settings.interval/1000

        # sample data while in sample-interval
        while time.monotonic() < sample_next:
          # TODO: check key-press
          sample = (5+math.sin(time.monotonic()),
                    25+math.cos(time.monotonic()))
          # TODO: check level
          s_data.add(sample)
          time.sleep(0.01)

        # TODO: check for successful sampling

        # sampling finished: log data and add to aggregators
        _,(v,a),_ = s_data.get()
        print("{},{},{}".format(time.monotonic(),v,a))
        m_data.add((v,a))
        d_data.add((v,a))

      # time to update the display
      _,(v,a),_ = d_data.get()
      self._values.set_values(v,a)
      self._values.show()

    # that's it, save results
    self._results.V = m_data.get(0)
    self._results.A = m_data.get(1)
