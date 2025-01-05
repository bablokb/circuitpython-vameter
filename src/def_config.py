# ----------------------------------------------------------------------------
# def_config.py: Default configuration-constants
#
# Don't change anything here directly, override in /user_config.py
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
#
# ----------------------------------------------------------------------------

import board

# select Dataprovider and DataLogger

#from INA219DataProvider import DataProvider # add this to user_config.py
#from INA260DataProvider import DataProvider # add this to user_config.py

#from ESP01Logger       import DataLogger    # add this to user_config.py
#from ESP32Logger       import DataLogger    # add this to user_config.py
#from SDCardLogger      import DataLogger    # add this to user_config.py

DEF_INT_SCALE  = 'ms'    # interval-scale: ms|s:    ms
DEF_INTERVAL   = 100     # sampling-interval:       100 in the given scale
DEF_UPDATE     = 1000    # display update-interval: 1000ms
DEF_OVERSAMPLE = 0       # oversampling:            0: use 1X, hide config
DEF_DURATION   = 0       # measurement-duration:    0s     (i.e. not limited)
DEF_VMIN       = 1.0     # threshold for V for start/stop of measurement
DEF_AMIN       = 0.0     # threshold for A for start/stop of measurement
DEF_PLOTS      = True    # create plots
DEF_EXIT       = False   # blinka: exit after measurement
DEF_TP_ORIENT  = 'P'     # touchpad orientation P|L
DEF_DISPLAY    = 'auto'  # auto|ssd1306|st7735r

BORDER = 1

# --- I2C   ------------------------------------------------------------------

if hasattr(board,'SDA'):
  PIN_SDA = board.SDA
  PIN_SCL = board.SCL

# --- I2C-display   ----------------------------------------------------------

OLED_ADDR   = 0x3C
OLED_WIDTH  = 128
OLED_HEIGHT = 64

# --- SPI-display   ----------------------------------------------------------

TFT_WIDTH  = 160
TFT_HEIGHT = 128
TFT_ROTATE = 270
TFT_BGR    = True

PIN_MOSI = getattr(board,'MOSI',None)
PIN_CLK  = getattr(board,'SCLK',None)
if not PIN_CLK:
  PIN_CLK  = getattr(board,'SCK',None)

# --- no defaults: must be set in board_config.py or in user_config.py   ------

PIN_CS  = None
PIN_DC  = None
PIN_RST = None

# --- UART-pins (only necessary for ESP-01)   ---------------------------------

if hasattr(board,'TX'):
  PIN_TX = board.TX
  PIN_RX = board.RX

# --- SPI-SD-card   -----------------------------------------------------------

PIN_SD_MISO = getattr(board,'MISO',None)
PIN_SD_MOSI = PIN_MOSI
PIN_SD_CLK  = PIN_CLK
PIN_SD_CS   = None   # set in board_config.py or user_config.py
