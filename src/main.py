# ----------------------------------------------------------------------------
# main.py: driver program vor VA-meter
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
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

from FakeDataProvider import DataProvider
from Touchpad import KeyEventProvider

# --- constants   ------------------------------------------------------------

DEF_INTERVAL = 100    # sampling-interval:       100ms
DEF_DURATION = 0      # measurement-duration:    0s     (i.e. not limited)
DEF_UPDATE   = 500    # display update-interval: 500ms

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

# --- ValueHolder class   ----------------------------------------------------

class ValueHolder:
  pass

# --- application class   ----------------------------------------------------

class VAMeter:
  """ application class """

  # --- constructor   --------------------------------------------------------

  def __init__(self):
    """ constructor """

    if not hasattr(board,'DISPLAY'):
      displayio.release_displays()

    i2c = busio.I2C(sda=PIN_SDA,scl=PIN_SCL)

    self.display = self._get_display(i2c)
    self.border  = OLED_BORDER

    self.settings = ValueHolder()
    self.settings.interval = DEF_INTERVAL
    self.settings.duration = DEF_DURATION
    self.settings.update   = DEF_UPDATE

    self.data_provider = DataProvider(self.settings)
    self.results        = ValueHolder()
    self.results.values = [[0,0,0] for i in range(self.data_provider.get_dim())]
    self.results.time   = 0

    try:
      self.key_events = KeyEventProvider(i2c,self.settings)
    except:
      self.key_events = None

    self._ready  = ReadyState(self)
    self._active = ActiveState(self)
    self._config = ConfigState(self)

  # --- initialize display   -------------------------------------------------

  def _get_display(self,i2c):
    """ initialize hardware """

    if hasattr(board,'DISPLAY') and board.DISPLAY:
      return board.DISPLAY
    else:
      try:
        display_bus = displayio.I2CDisplay(i2c, device_address=OLED_ADDR)
        return adafruit_displayio_ssd1306.SSD1306(display_bus,
                                                  width=OLED_WIDTH,
                                                  height=OLED_HEIGHT)
      except:
        return None

  # --- main loop   ----------------------------------------------------------

  def run(self):
    """ main loop """

    #self._config.run()
    while True:
      next_state = self._ready.run(self._active,self._config)
      next_state.run()

# --- main loop   ------------------------------------------------------------

app = VAMeter()
app.run()

