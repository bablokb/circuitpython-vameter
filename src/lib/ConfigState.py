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

    self._app   = app
    headings    = ['Interval:','Duration:','Update:']
    units       = ['ms','s','s']
    self._attr  = ['interval','duration','update']
    self._views = [ConfigView(app.display,app.border,
                              headings[i],
                              units[i])
                   for i in range(len(headings))]

  # --- update a setting   ----------------------------------------------------

  def _upd_value(self,nr):
    """ update value of current setting """

    value = getattr(self._app.settings,self._attr[nr])
    if int(value) == value:
      value = int(value)
    str_value = str(value)
    while True:
      print("value: %f (%s)" % (value,str_value))
      self._views[nr].set_value(value)
      self._views[nr].show()
      key = self._app.key_events.wait_for_key(self._app.key_events.KEYMAP_CONFIG)
      print("key: %s" % key)
      if key == 'NEXT':
        setattr(self._app.settings,self._attr[nr],value)
        return
      elif key == 'CLR':
        str_value = str_value[:-1]
        if str_value == '0.':
          str_value = ''
        value     = float(str_value) if len(str_value) else 0
      else:
        str_value = str_value+key
        value     = float(str_value) if str_value != '.' else 0
        if int(value) == value:
          value = int(value)

  # --- loop during config-state   --------------------------------------------

  def run(self):
    """ main-loop during config-state """

    if not self._app.display:
      return
    else:
      # loop over all settings
      for i in range(len(self._views)):
        self._upd_value(i)
