# ----------------------------------------------------------------------------
# board_config.py: board-specific configuration for pico_pi_base_w_rev2
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
#
# ----------------------------------------------------------------------------

import board

# I2C pins

PIN_SDA = board.SDA
PIN_SCL = board.SCL

# SPI/TFT pins

PIN_MOSI = board.MOSI
PIN_CLK  = board.SCLK
PIN_CS   = board.CE0
PIN_DC   = board.GPIO22
PIN_RST  = board.GPIO27

# UART

PIN_TX = board.TX
PIN_RX = board.RX

# SPI-SD-card

PIN_SD_MISO = board.MISO
PIN_SD_MOSI = PIN_MOSI
PIN_SD_CLK  = PIN_CLK
PIN_SD_CS   = board.SD_CS
