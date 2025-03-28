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

from Touchpad           import KeyEventProvider

if hasattr(board,'__blinka__'):
  # support functions for Blinka
  import BlinkaExtensions

# --- ValueHolder class   ----------------------------------------------------

class ValueHolder:
  pass

# --- configuration   --------------------------------------------------------

from def_config import settings as def_settings

try:
  if board.board_id.startswith("RASPBERRY_PI"):
    sys.path.insert(0,"./RASPBERRY_PI")
  else:
    sys.path.insert(0,"./"+board.board_id)
  from board_config import *
except:
  print("no board-specific config-file for %s, using defaults" % board.board_id)

try:
  from user_config import settings as user_settings
except Exception as ex:
  print("no user-configuration found, using defaults")
  user_settings = ValueHolder()

try:
  from user_config import DataProvider
except Exception as ex:
  print("no user-specific data-provider, using INA219DataProvider")
  from INA219DataProvider import DataProvider

try:
  from user_config import DataLogger
except Exception as ex:
  print("no user-specific data-logger, using SerialLogger")
  from SerialLogger import DataLogger

# --- application class   ----------------------------------------------------

class VAMeter:
  """ application class """

  # --- constructor   --------------------------------------------------------

  def __init__(self):
    """ constructor """

    # merge default and user-settings
    self.settings = def_settings
    self._merge_settings(user_settings)
    if hasattr(board,'__blinka__'):
      # change defaults from commandline arguments
      BlinkaExtensions.update_settings(self.settings)

    # set pins from board-configuration if not already set
    g_dict = globals()
    for attr in ['pin_scl', 'pin_sda', 'pin_tx', 'pin_rx',
                 'pind_miso', 'pin_mosi', 'pin_clk',
                 'pin_sd_miso', 'pin_sd_mosi', 'pin_sd_clk', 'pin_sd_cs',
                 'pin_tft_mosi', 'pin_tft_clk', 'pin_tft_cs',
                 'pin_tft_dc', 'pin_tft_rst',
                 'pin_app'
                 ]:
      if not getattr(self.settings,attr,None) and attr.upper() in g_dict:
        setattr(self.settings,attr,g_dict[attr.upper()])

    # initialize hardware and software objects
    if not hasattr(board,'DISPLAY'):
      displayio.release_displays()

    self.i2c = busio.I2C(sda=self.settings.pin_sda,
                         scl=self.settings.pin_scl,frequency=400000)

    if self.settings.shared_spi and self.settings.pin_clk:
      self.spi = busio.SPI(clock=self.settings.pin_clk,
                           MOSI=self.settings.pin_mosi,
                           MISO=self.settings.pin_miso)
    else:
      self.spi = None

    self.data_provider  = DataProvider(self.i2c,self.settings)
    self.logger         = DataLogger(self)

    # create value-holder for results
    self.results        = ValueHolder()
    self.results.values = [[0,0,0] for i in range(self.data_provider.get_dim())]
    self.results.time   = 0
    self.results.plots  = []

    self.display = self._get_display()
    if self.display:
      self.display.auto_refresh = False

    try:
      self.key_events = KeyEventProvider(i2c,self.settings)
    except:
      self.key_events = None

    self._ready  = ReadyState(self)
    self._active = ActiveState(self)
    if self.display:
      self._config = ConfigState(self)
    else:
      self._config = None

  # --- merge generic user settings   ----------------------------------------

  def _merge_settings(self,u_settings):
    """ merge generic user settings """

    for attr in u_settings.__dict__:
      if attr[:2] == '__':
        continue
      setattr(self.settings,attr,getattr(u_settings,attr))

  # --- initialize display   -------------------------------------------------

  def _get_display(self):
    """ initialize hardware """

    if not self.settings.display:  # run headless
      return None

    if self.settings.display == 'ssd1306':
      display_bus = displayio.I2CDisplay(
        self.i2c,
        device_address=self.settings.oled_addr)
      return adafruit_displayio_ssd1306.SSD1306(
        display_bus,
        width=self.settings.oled_width,
        height=self.settings.oled_height)
    elif self.settings.display == 'st7735r':
      if self.spi:
        spi = self.spi
      else:
        spi = busio.SPI(clock=self.settings.pin_tft_clk,
                        MOSI=self.settings.pin_tft_mosi)
      bus = displayio.FourWire(spi,command=self.settings.pin_tft_dc,
                               chip_select=self.settings.pin_tft_cs,
                               reset=self.settings.pin_tft_rst)
      return ST7735R(bus,width=self.settings.tft_width,
                     height=self.settings.tft_height,
                     rotation=self.settings.tft_rotate,
                     bgr=self.settings.tft_bgr)
    elif self.settings.display == 'auto':
      if hasattr(board,'DISPLAY') and board.DISPLAY:
        return board.DISPLAY
      else:
        # try OLED display first
        try:
          display_bus = displayio.I2CDisplay(
            self.i2c, device_address=self.settings.oled_addr)
          return adafruit_displayio_ssd1306.SSD1306(
            display_bus,
            width=self.settings.oled_width,
            height=self.settings.oled_height)
        except:
          pass
        # then try SPI-display
        try:
          if self.spi:
            spi = self.spi
          else:
            spi = busio.SPI(clock=self.settings.pin_tft_clk,
                            MOSI=self.settings.pin_tft_mosi)
          bus = displayio.FourWire(spi,
                                   command=self.settings.pin_tft_dc,
                                   chip_select=self.settings.pin_tft_cs,
                                   reset=self.settings.pin_tft_rst)
          return ST7735R(bus,width=self.settings.tft_width,
                         height=self.settings.tft_height,
                         rotation=self.settings.tft_rotate,
                         bgr=self.settings.tft_bgr)
        except:
          return None
    else:
      print(f"invalid value of settings.display: {self.settings.display}")
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
finally:
  try:
    app.logger.close()
  except:
    pass
