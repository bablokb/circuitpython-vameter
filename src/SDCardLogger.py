# ----------------------------------------------------------------------------
# SDCardLogger.py: log values to a SD-card
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
#
# ----------------------------------------------------------------------------

import os
import busio
import digitalio
import storage
import adafruit_sdcard

from LogWriter import LogWriter

class DataLogger(LogWriter):
  """ log data to a file on SD-card """

  # --- constructor   --------------------------------------------------------

  def __init__(self,app):
    """ constructor """
    super(DataLogger,self).__init__(app)

    # mount SD-card and open logfile
    spi    = busio.SPI(app.settings.pin_sd_clk,
                       app.settings.pin_sd_mosi,
                       app.settings.pin_sd_miso)
    cs     = digitalio.DigitalInOut(app.settings.pin_sd_cs)
    sdcard = adafruit_sdcard.SDCard(spi,cs)
    vfs    = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
    self._sdfile = None

  # --- open logger   --------------------------------------------------------

  def open(self):
    """ open logger """
    data_files = sorted([fname for fname in os.listdir("/sd")
                         if fname[:7] == 'vameter' and fname[-4:] == '.csv'],
                        reverse=True)
    if len(data_files):
      print(f"last file: {data_files[0]}")
      nr = int(data_files[0].split(".")[0].split("-")[1]) + 1
    else:
      nr = 1
    print(f"new number: {nr}")
    fname = f"/sd/vameter-{nr:04d}.csv"
    print(f"logfile: {fname}")
    self._sdfile = open(fname,"a")
    print(f"{fname} opened for logging")

  # --- close logger   -------------------------------------------------------

  def close(self):
    """ close logger """
    if self._sdfile:
      try:
        print("closing log-file")
        self._sdfile.close()
      except:
        pass

  # --- log implementation   -------------------------------------------------

  def log(self,msg):
    """ write to file """

    print(msg,end="")
    self._sdfile.write(msg)
