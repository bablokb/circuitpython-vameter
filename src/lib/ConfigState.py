# ----------------------------------------------------------------------------
# ConfigState.py: Handle config-state, i.e. display last results and enter
#                config or run-state depending on buttton input
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pico-cp-vameter
#
# ----------------------------------------------------------------------------

import time
from View import ConfigView

class ConfigState:
  """ manage config-state """

  # --- constructor   --------------------------------------------------------

  def __init__(self,app):
    """ constructor """

    self._app      = app
    self._settings = app.settings
    self._interval = ConfigView(app.display,app.border,'Interval:','ms')
    self._duration = ConfigView(app.display,app.border,'Duration:','s')
    self._update   = ConfigView(app.display,app.border,'Update:','s')

  # --- loop during config-state   --------------------------------------------

  def run(self):
    """ main-loop during config-state """

    if self._app.display:
      self._interval.set_value(self._settings.interval)
      self._interval.show()
      time.sleep(3)

      self._duration.set_value(self._settings.duration)
      self._duration.show()
      time.sleep(3)

      self._update.set_value(self._settings.update)
      self._update.show()
      time.sleep(3)
