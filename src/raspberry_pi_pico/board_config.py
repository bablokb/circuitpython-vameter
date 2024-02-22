# ----------------------------------------------------------------------------
# board_config.py: board-specific configuration for raspberry_pi_pico
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
#
# ----------------------------------------------------------------------------

import board

# I2C pins

PIN_SDA = board.GP2
PIN_SCL = board.GP3

# SPI/TFT pins

PIN_MOSI = board.GP15
PIN_CLK  = board.GP14
PIN_CS   = board.GP9
PIN_DC   = board.GP10
PIN_RST  = board.GP11

# UART

PIN_TX = board.GP0
PIN_RX = board.GP1

# SPI-SD-card

PIN_SD_MISO = board.GP12
PIN_SD_MOSI = PIN_MOSI
PIN_SD_CLK  = PIN_CLK
PIN_SD_CS   = board.GP8
