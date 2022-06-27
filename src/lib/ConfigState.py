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
from Scales import *

class ConfigState:
  """ manage config-state """

  # --- constructor   --------------------------------------------------------

  def __init__(self,app):
    """ constructor """

    self._app   = app
    headings    = ['Int-Scale:','Interval:','Duration:','Update:']
    units       = ["",app.settings.tm_scale,
                   dur_scale(app.settings.tm_scale),'ms']
    self._attr  = ['tm_scale','interval','duration','update']
    if app.settings.oversample > 0:
      headings.append('Oversample:')
      units.append('X')
      self._attr.append('oversample')
    self._views = [ConfigView(app.display,app.border,
                              headings[i],
                              units[i])
                   for i in range(len(headings))]
    self._int_view = self._views[1]
    self._dur_view = self._views[2]

  # --- update a setting   ----------------------------------------------------

  def _upd_value(self,nr):
    """ update value of current setting """

    value = str(getattr(self._app.settings,self._attr[nr]))
    while True:
      self._views[nr].set_value(value)
      self._views[nr].show()
      key = self._app.key_events.wait_for_key(self._app.key_events.KEYMAP_CONFIG)
      if key == 'NEXT':
        if nr == 0:
          setattr(self._app.settings,self._attr[nr],value)     # scale is a string
          self._int_view.set_unit(value)
          self._dur_view.set_unit(dur_scale(value))
        else:
          setattr(self._app.settings,self._attr[nr],int(value))
        return
      elif key == 'CLR':
        if nr == 0:
          value = 'ms'
        elif len(value) > 1:
          value = value[:-1]
        else:
          value = '0'
      elif value == '0':
        value = key
      elif nr == 0:
        index = min(int(key),len(INT_SCALES)) - 1
        value = list(INT_SCALES.items())[index][0]
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
