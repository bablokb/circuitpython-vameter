# ----------------------------------------------------------------------------
# ESP32Logger.py: log values using (builtin) ESP32. Tested with Qt Py ESP32-S2
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
#
# ----------------------------------------------------------------------------

import socketpool
import wifi
from LogWriter import LogWriter

try:
  from secrets import secrets
except ImportError:
  print("WiFi settings need the file secrets.py, see documentation")
  raise


class DataLogger(LogWriter):
  """ log data using an ESP32 """

  # --- constructor   --------------------------------------------------------

  def __init__(self,app):
    """ constructor: """
    super(DataLogger,self).__init__(app)
    self._init_esp32()

  # --- initialze ESP32, connect to AP   -------------------------------------

  def _init_esp32(self):
    """ initialize ESP32 """

    # try to connect
    retry = secrets["retry"]
    while True:
      if retry == 0:
        raise RuntimeError("failed to connect to %s" % secrets["ssid"])
      try:
        wifi.radio.connect(secrets["ssid"], secrets["password"])
        break
      except Exception as e:
        retry -= 1
        continue

    # setup connection
    pool = socketpool.SocketPool(wifi.radio)
    self._transport = secrets["transport"]
    if self._transport == 'UDP':
      self._socket = pool.socket(family=socketpool.SocketPool.AF_INET,
                                 type=socketpool.SocketPool.SOCK_DGRAM)
      self._dest = (secrets["remote_ip"],secrets["remote_port"])
    else:
      self._socket = pool.socket(family=socketpool.SocketPool.AF_INET,
                                 type=socketpool.SocketPool.SOCK_STREAM)

  # --- send data   ----------------------------------------------------------

  def log(self,msg):
    """ send the given message """
    try:
      if self._transport == 'UDP':
        self._socket.sendto(msg.encode('utf-8'),self._dest)
      else:
        pass
    except:
      # can't do much here, go on so local measurement continues
      pass
