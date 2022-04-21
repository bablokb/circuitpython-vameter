# ----------------------------------------------------------------------------
# Touchpad.py: provide key-events using a MPR121-based 4x3 touchpad
#
# To port this provider you must implement the methods
#   - wait_for_key() -> key
#   - is_key_pressed(key1..keyN) -> key or None
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
#
# ----------------------------------------------------------------------------

import time
import adafruit_mpr121

class KeyEventProvider:
  """ provide key events """

  DEBOUNCE_TIME = 0.200

  KEYMAP_READY = {
    0: 'START',
    4: 'CONFIG',
    6: 'TOGGLE'
    }
  KEYMAP_ACTIVE = {
    8: 'STOP',
    6: 'TOGGLE'
    }
  KEYMAP_CONFIG = {
    0: 'NEXT',   4: '0',     8: 'CLR',    # set 4: 'SHIFT' if '.' is needed
    1: '7',      5: '8',     9: '9',
    2: '4',      6: '5',    10: '6',
    3: '1',      7: '2',    11: '3'
    }
  KEYMAP_SHIFT = {
    0: 'NEXT',
    4: 'SHIFT',
    8: 'CLR',
    5: '0',
    9: '.'
    }

  # --- constructor   --------------------------------------------------------

  def __init__(self,i2c,settings):
    """ constructor """

    self._settings = settings
    self._mpr121   = adafruit_mpr121.MPR121(i2c)
    self._last_key = (-1,time.monotonic())

  # --- get key (with debounce-control)   ------------------------------------

  def _get_key(self):
    """ return key or None if within debounce-interval """

    touched = self._mpr121.touched_pins
    if True not in touched:
      return None

    # get current key and check for bouncing
    index = touched.index(True)
    t     = time.monotonic()
    if index == self._last_key[0] and t < (
                         self._last_key[1] + KeyEventProvider.DEBOUNCE_TIME):
      return None
    else:
      self._last_key = (index,time.monotonic())
      return index

  # --- wait for a key   -----------------------------------------------------

  def wait_for_key(self,keymap):
    """ wait for key-press and return it """

    normal_keymap = keymap
    shift         = False
    while True:
      # get current key and check for bouncing
      index = self._get_key()

      # check for correct key
      if index not in keymap.keys():   # implicitly checks for None
        continue

      # process shift
      if keymap[index] != 'SHIFT':
        return keymap[index]
      elif shift:
        keymap = normal_keymap
        shift  = False
      else:
        keymap = KeyEventProvider.KEYMAP_SHIFT
        shift  = True

  # --- check specific keys   -------------------------------------------------

  def is_key_pressed(self,keymap):
    """ check keys and return the key or None """

    index = self._get_key()
    if index not in keymap.keys():
      return None
    else:
      return keymap[index]
