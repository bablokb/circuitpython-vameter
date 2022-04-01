# ----------------------------------------------------------------------------
# main.py: driver program vor VA-meter
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pico-cp-vameter
#
# ----------------------------------------------------------------------------

import board
import busio
import displayio
import time

import adafruit_displayio_ssd1306

from ReadyState  import ReadyState
from ConfigState import ConfigState
from ActiveState import ActiveState

# --- constants   ------------------------------------------------------------

OLED_ADDR   = 0x3C
OLED_WIDTH  = 128
OLED_HEIGHT = 64
OLED_BORDER = 1

if board.board_id == 'raspberry_pi_pico':
  PIN_SDA = board.GP18
  PIN_SCL = board.GP19
elif hasattr(board,'SDA'):
  PIN_SDA = board.SDA
  PIN_SCL = board.SCL

# --- application class   ----------------------------------------------------

class VAMeter:
  """ application class """

  # --- constructor   --------------------------------------------------------

  def __init__(self):
    """ constructor """

    self._display     = self._get_display()
    self._ready       = ReadyState(self._display,OLED_BORDER)
    self._active      = ActiveState(self._display,OLED_BORDER)
    self._config      = ConfigState(self._display,OLED_BORDER)

  # --- initialize display   -------------------------------------------------

  def _get_display(self):
    """ initialize hardware """

    displayio.release_displays()
    if hasattr(board,'DISPLAY') and board.DISPLAY:
      return board.DISPLAY
    else:
      try:
        i2c = busio.I2C(sda=PIN_SDA,scl=PIN_SCL)
        display_bus = displayio.I2CDisplay(i2c, device_address=OLED_ADDR)
        return adafruit_displayio_ssd1306.SSD1306(display_bus,
                                                  width=OLED_WIDTH,
                                                  height=OLED_HEIGHT)
      except:
        return None

  # --- main loop   ----------------------------------------------------------

  def run(self):
    """ main loop """

    self._config.run()
    while True:
      next_state = self._ready.run(self._active,self._config)
      next_state.run()

# --- main loop   ------------------------------------------------------------

app = VAMeter()
app.run()

