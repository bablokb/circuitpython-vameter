# ----------------------------------------------------------------------------
# main.py: driver program for VA-meter
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
#
# ----------------------------------------------------------------------------

import board
import sys
import busio
import displayio
import time

import adafruit_displayio_ssd1306          # I2C-OLED display
from adafruit_st7735r import ST7735R       # SPI-TFT  display

from ReadyState  import ReadyState
from ConfigState import ConfigState
from ActiveState import ActiveState

#from FakeDataProvider import DataProvider
from INA219DataProvider import DataProvider
from Touchpad           import KeyEventProvider

from SerialLogger       import DataLogger
#from ESP01Logger       import DataLogger
#from ESP32Logger       import DataLogger

if hasattr(board,'__blinka__'):
  # support functions for Blinka
  import BlinkaExtensions

# --- configuration   --------------------------------------------------------

from def_config import *

try:
  if board.board_id.startswith("RASPBERRY_PI"):
    sys.path.insert(0,"./RASPBERRY_PI")
  else:
    sys.path.insert(0,"./"+board.board_id)
  from board_config import *
except:
  print("no board-specific config-file for %s, using defaults" % board.board_id)

try:
  from user_config import *
except:
  print("no user-specific config-file")

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

    i2c = busio.I2C(sda=PIN_SDA,scl=PIN_SCL,frequency=400000)

    self.display = self._get_display(i2c)
    if self.display:
      self.display.auto_refresh = False
    self.border  = BORDER

    self.settings = ValueHolder()
    self.settings.interval   = DEF_INTERVAL
    self.settings.int_scale  = DEF_INT_SCALE
    self.settings.oversample = DEF_OVERSAMPLE
    self.settings.duration   = DEF_DURATION
    self.settings.update     = DEF_UPDATE
    self.settings.plots      = DEF_PLOTS
    self.settings.exit       = DEF_EXIT
    self.settings.tp_orient  = DEF_TP_ORIENT
    if hasattr(board,'__blinka__'):
      # change defaults from commandline arguments
      BlinkaExtensions.update_settings(self.settings)

    self.settings.pin_tx     = PIN_TX
    self.settings.pin_rx     = PIN_RX

    self.data_provider  = DataProvider(i2c,self.settings)
    self.logger         = DataLogger(self)

    self.results        = ValueHolder()
    self.results.values = [[0,0,0] for i in range(self.data_provider.get_dim())]
    self.results.time   = 0
    self.results.plots  = []

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
      # try OLED display first
      try:
        display_bus = displayio.I2CDisplay(i2c, device_address=OLED_ADDR)
        return adafruit_displayio_ssd1306.SSD1306(display_bus,
                                                  width=OLED_WIDTH,
                                                  height=OLED_HEIGHT)
      except:
        pass
      # then try SPI-display
      try:
        spi = busio.SPI(clock=PIN_CLK,MOSI=PIN_MOSI)
        bus = displayio.FourWire(spi,command=PIN_DC,chip_select=PIN_CS,
                                 reset=PIN_RST)
        return ST7735R(bus,width=TFT_WIDTH,height=TFT_HEIGHT,
                       rotation=TFT_ROTATE,bgr=TFT_BGR)
      except:
        return None

  # --- main loop   ----------------------------------------------------------

  def run(self):
    """ main loop """

    if not self.key_events:
      # no keypad, only one iteration without config
      self._active.run()
      self._ready.run(self._active,self._config)      # display results
    else:
      while True:
        next_state = self._ready.run(self._active,self._config)
        if next_state is None:
          break
        next_state.run()

# --- main loop   ------------------------------------------------------------

try:
  app = VAMeter()
  app.run()
except KeyboardInterrupt:
  if hasattr(board,'__blinka__'):
    # finish program without backtrace
    pass
  else:
    raise
