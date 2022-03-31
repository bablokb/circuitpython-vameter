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

from View import ValuesView

# --- constants   ------------------------------------------------------------

OLED_ADDR   = 0x3C
OLED_WIDTH  = 128
OLED_HEIGHT = 64
OLED_BORDER = 1
PIN_SDA     = board.GP18
PIN_SCL     = board.GP19

# --- application class   ----------------------------------------------------

class VAMeter:
  """ application class """

  # --- constructor   --------------------------------------------------------

  def __init__(self):
    """ constructor """

    self._display     = self._get_display()
    self.values_view  = ValuesView(self._display,OLED_BORDER)
    self._view        = self.values_view

  # --- initialize display   -------------------------------------------------

  def _get_display(self):
    """ initialize hardware """

    displayio.release_displays()
    i2c = busio.I2C(sda=PIN_SDA,scl=PIN_SCL)
    display_bus = displayio.I2CDisplay(i2c, device_address=OLED_ADDR)
    return adafruit_displayio_ssd1306.SSD1306(display_bus,
                                              width=OLED_WIDTH,
                                              height=OLED_HEIGHT)

  # --- show current view   --------------------------------------------------

  def show(self):
    """ update display and show current view """

    self._view.show()

# --- main loop   ------------------------------------------------------------

app = VAMeter()
app.show()
time.sleep(3)

v = 4.95
a = 0
while True:
  time.sleep(2)
  app.values_view.set_values(v,a)
  v += 0.1
  a += 1
