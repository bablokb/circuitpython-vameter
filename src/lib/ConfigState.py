# ----------------------------------------------------------------------------
# ConfigState.py: Handle config-state, i.e. display last results and enter
#                config or run-state depending on buttton input
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
#
# ----------------------------------------------------------------------------

import time
from View import ConfigView

class ConfigState:
  """ manage config-state """

  # --- constructor   --------------------------------------------------------

  def __init__(self,app):
    """ constructor """

    self._app   = app
    headings    = ['Interval:','Duration:','Update:']
    units       = ['ms','s','ms']
    self._attr  = ['interval','duration','update']
    self._views = [ConfigView(app.display,app.border,
                              headings[i],
                              units[i])
                   for i in range(len(headings))]

  # --- update a setting   ----------------------------------------------------

  def _upd_value(self,nr):
    """ update value of current setting """

    value = str(getattr(self._app.settings,self._attr[nr]))
    while True:
      self._views[nr].set_value(value)
      self._views[nr].show()
      key = self._app.key_events.wait_for_key(self._app.key_events.KEYMAP_CONFIG)
      if key == 'NEXT':
        setattr(self._app.settings,self._attr[nr],int(value))
        return
      elif key == 'CLR':
        if len(value) > 1:
          value = value[:-1]
        else:
          value = '0'
      elif value == '0':
        value = key
      else:
        value = value+key

  # --- loop during config-state   --------------------------------------------

  def run(self):
    """ main-loop during config-state """

    if not self._app.display:
      return
    else:
      # loop over all settings
      for i in range(len(self._views)):
        self._upd_value(i)
