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

from View import ValuesView, ResultView

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
    self._view        = None
    self.values_view  = ValuesView(self._display,OLED_BORDER)
    self.resV_view    = ResultView(self._display,OLED_BORDER,'V')
    self.resA_view    = ResultView(self._display,OLED_BORDER,'mA')

  # --- initialize display   -------------------------------------------------

  def _get_display(self):
    """ initialize hardware """

    displayio.release_displays()
    i2c = busio.I2C(sda=PIN_SDA,scl=PIN_SCL)
    display_bus = displayio.I2CDisplay(i2c, device_address=OLED_ADDR)
    return adafruit_displayio_ssd1306.SSD1306(display_bus,
                                              width=OLED_WIDTH,
                                              height=OLED_HEIGHT)

  # --- set current view   ---------------------------------------------------

  def set_view(self,view):
    """ set current view """
    self._view = view

  # --- show current view   --------------------------------------------------

  def show(self):
    """ update display and show current view """

    self._view.show()

# --- main loop   ------------------------------------------------------------

app = VAMeter()

app.resV_view.set_values(4.95,5.01,1025.25)
app.resA_view.set_values(18,1014.6,1025.25)
app.set_view(app.resV_view)
app.show()

time.sleep(5)
app.set_view(app.resA_view)
app.show()
time.sleep(5)


v = 4.95
a = 0
app.values_view.set_values(v,a)
app.set_view(app.values_view)
app.show()

while True:
  time.sleep(2)
  app.values_view.set_values(v,a)
  v += 0.1
  a += 1
