# ----------------------------------------------------------------------------
# board_config.py: board-specific configuration for various Raspberry Pi models
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

PIN_TFT_CS = board.CE0
