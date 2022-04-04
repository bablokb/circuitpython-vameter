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

    if not self._app.display:
      # no config without display, so just start
      return active

    # set results and show first view
    cur_view = 0
    n_views  = len(self._views)
    for index,result in enumerate(self._app.results):
      self._views[index].set_values(*result)
    self._views[cur_view].show()

    # query key and process
    while True:
      key = self._app.key_events.wait_for_key(self._app.key_events.KEYMAP_READY)
      if key == 'START':
        return active
      elif key == 'CONFIG':
        return config
      else:
        cur_view = (cur_view+1) % n_views
        self._views[cur_view].show()
        time.sleep(0.1)
