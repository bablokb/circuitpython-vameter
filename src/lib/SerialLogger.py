# ----------------------------------------------------------------------------
# SerialLogger.py: log values to the serial console
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
#
# ----------------------------------------------------------------------------

from LogWriter import LogWriter

class DataLogger(LogWriter):
  """ log data to the serial console """

  # --- constructor   --------------------------------------------------------

  def __init__(self,app):
    """ constructor: just pass the builtin print()-function to base-class """
    super(DataLogger,self).__init__(app,print)
