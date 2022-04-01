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
from View import ValuesView

class ActiveState:
  """ manage active-state """

  # --- constructor   --------------------------------------------------------

  def __init__(self,app):
    """ constructor """

    self._app    = app
    self._values = ValuesView(app.display,app.border)

  # --- loop during ready-state   --------------------------------------------

  def run(self):
    """ main-loop during active-state """

    v = 4.95
    a = 0
    self._values.set_values(v,a)
    self._values.show()

    while True:
      time.sleep(2)
      self._values.set_values(v,a)
      v += 0.1
      a += 1
