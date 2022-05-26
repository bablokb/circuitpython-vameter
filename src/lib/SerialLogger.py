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
    """ constructor """
    super(DataLogger,self).__init__(app)

  # --- log implementation   -------------------------------------------------

  def log(self,msg):
    """ just pass the string to the builtin print()-function """

    print(msg,end="")
