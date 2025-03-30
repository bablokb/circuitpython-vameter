# ----------------------------------------------------------------------------
# board_config.py: board-specific configuration for picow_pi_base_rev2
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
#
# ----------------------------------------------------------------------------

import board

# define pins from non-standard board-pins
# other pins are user-specific
# requires (default) settings.shared_spi = True

PIN_SCK    = board.SCLK
PIN_TFT_CS = board.CE0
PIN_SD_CS  = board.SD_CS
