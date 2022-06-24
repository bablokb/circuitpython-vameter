# ----------------------------------------------------------------------------
# main.py: driver program vor VA-meter
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
#
# ----------------------------------------------------------------------------

import gc
import board
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

# --- constants   ------------------------------------------------------------

DEF_TM_SCALE   = 'ms'     # time-scale: ms|s:        ms
if DEF_TM_SCALE == 'ms':
  DEF_INTERVAL   = 100    # sampling-interval:       100ms
  DEF_UPDATE     = 1000   # display update-interval: 1000ms
else:
  DEF_INTERVAL   = 60     # sampling-interval:       60s
  DEF_UPDATE     = 60     # display update-interval: 60s

DEF_OVERSAMPLE = 0        # oversampling:            0: use 1X, hide config
DEF_DURATION   = 0        # measurement-duration:    0s     (i.e. not limited)
DEF_PLOTS      = True     # create plots
DEF_EXIT       = False    # blinka: exit after measurement
BORDER = 1

# for the I2C-display   ---------------------------------

OLED_ADDR   = 0x3C
OLED_WIDTH  = 128
OLED_HEIGHT = 64

# I2C pins
if board.board_id == 'raspberry_pi_pico':
  PIN_SDA = board.GP2
  PIN_SCL = board.GP3
#  PIN_SDA = board.GP16
#  PIN_SCL = board.GP17
elif board.board_id == 'adafruit_qtpy_esp32s2':
  # use I2C from Stemma/Qt
  PIN_SDA = board.SDA1
  PIN_SCL = board.SCL1
elif hasattr(board,'SDA'):
  PIN_SDA = board.SDA
  PIN_SCL = board.SCL
else:
  # adapt to your MCU
  pass

# for the SPI-display   ---------------------------------

TFT_WIDTH  = 160
TFT_HEIGHT = 128
TFT_ROTATE = 270
TFT_BGR    = True

# SPI pins
if board.board_id == 'raspberry_pi_pico':
  PIN_CLK  = board.GP14
  PIN_MOSI = board.GP15
else:
  if hasattr(board,'MOSI'):
    PIN_MOSI = board.MOSI
  else:
    # adapt to your MCU
    PIN_MOSI = None
  if hasattr(board,'SCLK'):
    PIN_CLK = board.SCLK
  elif hasattr(board,'SCK'):
    PIN_CLK = board.SCK
  else:
    # adapt to your MCU
    PIN_CLK = None

# additional pins for TFT
if hasattr(board,'__blinka__'):
  # assume Raspberry Pi, change if required
  PIN_CS  = board.CE0
  PIN_DC  = board.D25
  PIN_RST = board.D24
elif board.board_id == 'raspberry_pi_pico':
  PIN_CS  = board.GP9
  PIN_DC  = board.GP10
  PIN_RST = board.GP11
else:
  # adapt to your MCU
  PIN_CS  = None
  PIN_DC  = None
  PIN_RST = None

# --- for UART-based components (e.g. ESP01, HC-05)   ------------------------
# (this is for optional components, see docs)

if board.board_id == 'raspberry_pi_pico':
  PIN_TX = board.GP0
  PIN_RX = board.GP1
elif hasattr(board,'TX'):
  PIN_TX = board.TX
  PIN_RX = board.RX
else:
  # adapt to your MCU
  PIN_TX = None
  PIN_RX = None

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
    self.settings.tm_scale   = DEF_TM_SCALE
    self.settings.oversample = DEF_OVERSAMPLE
    self.settings.duration   = DEF_DURATION
    self.settings.update     = DEF_UPDATE
    self.settings.plots      = DEF_PLOTS
    self.settings.exit       = DEF_EXIT
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

    try:
      self.key_events = KeyEventProvider(i2c,self.settings)
    except:
      self.key_events = None

    self._ready  = ReadyState(self)
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
      self._active = ActiveState(self)
      self._active.run()
      self._ready.run(self._active,self._config)      # display results
    else:
      while True:
        self._active = ActiveState(self)
        next_state = self._ready.run(self._active,self._config)
        if next_state is None:
          break
        gc.collect()
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
