# ----------------------------------------------------------------------------
# ReadyState.py: Handle ready-state, i.e. display last results and enter
#                config or run-state depending on buttton input
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pico-cp-vameter
#
# ----------------------------------------------------------------------------

import time
from View import ResultView

class ReadyState:
  """ manage ready-state """

  # --- constructor   --------------------------------------------------------

  def __init__(self,app):
    """ constructor """

    self._app     = app
    self._views   = []
    units = app.data_provider.get_units()
    for unit in units:
      self._views.append(ResultView(app.display,app.border,unit))

  # --- loop during ready-state   --------------------------------------------

  def run(self,active,config):
    """ main-loop during ready-state """

    if self._app.display:
      for index,result in enumerate(self._app.results):
        self._views[index].set_values(*result)
        self._views[index].show()
        time.sleep(3)

    return active
