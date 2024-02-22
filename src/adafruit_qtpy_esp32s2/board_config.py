# ----------------------------------------------------------------------------
# board_config.py: board-specific configuration for adafruit_qtpy_esp32s2
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
#
# ----------------------------------------------------------------------------

import board

PIN_SDA = board.SDA1
PIN_SCL = board.SCL1

# use standard pins of SD-card BFF

PIN_SD_MISO = board.MISO
PIN_SD_MOSI = board.MOSI
PIN_SD_CLK  = board.SCK
PIN_SD_CS   = board.TX
