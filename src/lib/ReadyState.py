# ----------------------------------------------------------------------------
# ReadyState.py: Handle ready-state, i.e. display last results and enter
#                config or run-state depending on buttton input
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pico-cp-vameter
#
# ----------------------------------------------------------------------------

import time
from View import ResultView

class ReadyState:
  """ manage ready-state """

  # --- constructor   --------------------------------------------------------

  def __init__(self,display,border):
    """ constructor """

    self._display = display
    self.result_V = ResultView(self._display,border,'V')
    self.result_A = ResultView(self._display,border,'mA')

  # --- loop during ready-state   --------------------------------------------

  def run(self):
    """ main-loop during ready-state """

    self.result_V.set_values(4.95,5.01,1025.25)
    self.result_V.show()
    time.sleep(5)

    self.result_A.set_values(18,1014.6,1025.25)
    self.result_A.show()
    time.sleep(5)
