# ----------------------------------------------------------------------------
# ESP01Logger.py: log values using an ESP-01S
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
#
# ----------------------------------------------------------------------------

DEBUGFLAG=False

import busio
import time

from adafruit_espatcontrol import (
  adafruit_espatcontrol,
  adafruit_espatcontrol_wifimanager,
)

from LogWriter import LogWriter

try:
  from secrets import secrets
except ImportError:
  print("WiFi settings need the file secrets.py, see documentation")
  raise


class DataLogger(LogWriter):
  """ log data using an ESP-01S """

  # --- constructor   --------------------------------------------------------

  def __init__(self,app):
    """ constructor: """
    super(DataLogger,self).__init__(app)
    self._init_esp01()

  # --- initialze ESP-01, connect to AP and to remote-port   -----------------

  def _init_esp01(self):
    """ initialize ESP-01 """

    uart = busio.UART(self.app.settings.pin_tx,
                      self.app.settings.pin_rx,
                      baudrate=11520,receiver_buffer_size=2048)

    self._esp = adafruit_espatcontrol.ESP_ATcontrol(
      uart,115200,reset_pin=None,rts_pin=None,debug=DEBUGFLAG)
    wifi = adafruit_espatcontrol_wifimanager.ESPAT_WiFiManager(
      self._esp,secrets,None)

    # try to connect
    retry = secrets["retry"]
    while True:
      if retry == 0:
        raise RuntimeError("failed to connect to %s" % secrets["ssid"])
      try:
        wifi.connect()
        break
      except Exception as e:
        retry -= 1
        continue

    # setup connection
    retry = secrets["retry"]
    while True:
      if retry == 0:
        raise RuntimeError(
          "failed to connect to %s:%d" %
          (secrets["remote_ip"],secrets["remote_port"]))
      try:
        if self._esp.socket_connect(secrets["transport"],
                                    secrets["remote_ip"],secrets["remote_port"]):
          break
        else:
          time.sleep(1)
      except Exception:
        pass
      retry -= 1

  # --- send data   ----------------------------------------------------------

  def log(self,msg):
    """ send the given message """
    try:
      self._esp.socket_send(msg.encode('utf-8'))
    except:
      # can't do much here, go on so local measurement continues
      pass
