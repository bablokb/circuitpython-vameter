# ----------------------------------------------------------------------------
# FakeDataProvider.py: emulate data-provider (for tests)
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pico-cp-vameter
#
# ----------------------------------------------------------------------------

import time
import math

class DataProvider:
  """ provide (fake) data """

  # --- constructor   --------------------------------------------------------

  def __init__(self,settings):
    """ constructor """

    self._settings = settings

  # --- return dimensions of data   ------------------------------------------

  def get_dim(self):
    """ dimension of data """
    return 2

  # --- log-format   ---------------------------------------------------------

  def get_fmt(self):
    """ return format for data, must include placeholder for timestamp """
    return "{0:.1f},{1:.2f},{2:.1f}"

  # --- provide data   -------------------------------------------------------

  def get_data(self):
    """ yield the next measurement """

    time.sleep(0.01)
    t = time.monotonic()
    return (5+t/10+math.sin(t),25+t/10+math.cos(t))
