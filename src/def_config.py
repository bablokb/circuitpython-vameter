# ----------------------------------------------------------------------------
# def_config.py: Default configuration-constants
#
# Don't change anything here directly, copy this file to user_config.py
# and change as necessary (delete all lines not touched)
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
#
# ----------------------------------------------------------------------------

import board

# --- select Dataprovider (add one to user_config.py)   ----------------------

#from INA219DataProvider import DataProvider
#from INA260DataProvider import DataProvider
#from INA3221DataProvider import DataProvider

# --- select DataLogger (default is SerialLogger)   --------------------------

#from UDPLogger       import DataLogger
#from SDCardLogger    import DataLogger

# --- helper-class for settings   --------------------------------------------

class ValueHolder:
  pass

# --- settings   -------------------------------------------------------------

settings = ValueHolder()
settings.interval   = 100     # sampling-interval: 100 in the given scale
settings.int_scale  = 'ms'    # interval-scale: ms|s: ms
settings.oversample = 0       # oversampling: 0: use 1X, hide config
settings.duration   = 0       # measurement-duration: 0s (i.e. not limited)
settings.v_min      = 1.0     # threshold for V for start/stop of measurement
settings.a_min      = 0.0     # threshold for A for start/stop of measurement
settings.update     = 1000    # display update-interval: 1000ms
settings.plots      = True    # create plots
settings.exit       = False   # blinka: exit after measurement
settings.tp_orient  = 'P'     # touchpad orientation P|L
settings.display    = 'auto'  # auto|ssd1306|st7735r|None
settings.border     = 1       # draw 1px border on display

# --- pins   -----------------------------------------------------------------

# note: some pins will be set automatically from board-config if available,
#       e.g. SDA, SCL, MISO, MOSI, SCK
#
# Pins explicitely set here will override defaults from board-config

settings.pin_sda     = None
settings.pin_scl     = None

settings.pin_tx      = None
settings.pin_rx      = None

settings.shared_spi  = True  # a shared SPI-bus will use the following pins
settings.pin_miso    = None
settings.pin_mosi    = None
settings.pin_sck     = None

settings.pin_sd_miso = None  # only needed for non-shared SPI-bus
settings.pin_sd_mosi = None  # only needed for non-shared SPI-bus
settings.pin_sd_sck  = None  # only needed for non-shared SPI-bus
settings.pin_sd_cs   = None

settings.pin_tft_mosi = None  # only needed for non-shared SPI-bus
settings.pin_tft_sck  = None  # only needed for non-shared SPI-bus
settings.pin_tft_cs   = None
settings.pin_tft_dc   = None
settings.pin_tft_rst  = None

settings.pins_app    = None

# --- I2C-display   ----------------------------------------------------------

settings.oled_addr   = 0x3C
settings.oled_width  = 128
settings.oled_height = 64

# --- SPI-display   ----------------------------------------------------------

settings.tft_width  = 160
settings.tft_height = 128
settings.tft_rotate = 270
settings.tft_bgr    = True

# --- INA219-defaults   ------------------------------------------------------

settings.ina219_addr  = 0x40 # default I2C-address
settings.ina219_calib = 1    # range: 32V/1A, resolution: 244µA
settings.ina219_adc   = 6    # ADCResolution.ADCRES_12BIT_8S

# --- INA260-defaults   ------------------------------------------------------

settings.ina260_addr  = 0x40 # default I2C-address
settings.ina260_count = 16   # internal oversampling
settings.ina260_ctime = 1    # ConversionTime.TIME_204_us

# --- INA3221-defaults   -----------------------------------------------------

settings.ina3221_addr     = 0x40  # default I2C-address
settings.ina3221_channels = 111   # channel-mask: all three channels
settings.ina3221_count    = 16    # internal oversampling
settings.ina3221_ctime    = 1     # ConversionTime.TIME_204_us
