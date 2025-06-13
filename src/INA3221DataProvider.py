# ----------------------------------------------------------------------------
# INA3221DataProvider.py: query data from INA3221 (I2C-Chip)
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
# ----------------------------------------------------------------------------

import time
from adafruit_ina3221 import CONV_TIME as ConversionTime
from adafruit_ina3221 import AVG_MODE as AveragingCount
from adafruit_ina3221 import INA3221

# rolling average count
AVG_COUNT = {
     1: AveragingCount.AVG_1_SAMPLE,
     4: AveragingCount.AVG_4_SAMPLES,
    16: AveragingCount.AVG_16_SAMPLES,
    64: AveragingCount.AVG_64_SAMPLES,
   128: AveragingCount.AVG_128_SAMPLES,
   256: AveragingCount.AVG_256_SAMPLES,
   512: AveragingCount.AVG_512_SAMPLES,
  1024: AveragingCount.AVG_1024_SAMPLES,
  }

# conversion time for measurement
CONV_TIME = [
  ConversionTime.CONV_TIME_140US,     # 0
  ConversionTime.CONV_TIME_204US,     # 1
  ConversionTime.CONV_TIME_332US,     # 2
  ConversionTime.CONV_TIME_588US,     # 3
  ConversionTime.CONV_TIME_1MS,       # 4
  ConversionTime.CONV_TIME_2MS,       # 5
  ConversionTime.CONV_TIME_4MS,       # 6
  ConversionTime.CONV_TIME_8MS,       # 7
  ]

CHANNELS = [1, 10, 11, 100, 101, 110, 111 ]

class DataProvider:
  """ provide data """

  _dim   = 6
  _units = ['V','mA']*3
  _fmt   = [f"{{{i}:.3f}}" for i in range(1,7)]

  # --- constructor   --------------------------------------------------------

  def __init__(self,i2c,settings):
    """ constructor """

    self._settings = settings
    if not hasattr(self._settings,"ina3221_channels"):
      setattr(self._settings,"ina3221_channels",111)
    if not hasattr(self._settings,"ina3221_count"):
      setattr(self._settings,"ina3221_count",4)
    if not hasattr(self._settings,"ina3221_ctime"):
      setattr(self._settings,"ina3221_ctime",2)      # ConversionTime.TIME_332_us

    addr = getattr(self._settings,"ina3221_addr",0x40)
    self._ina3221 = INA3221(i2c,addr,enable=[])      # all channels disabled
    self.reset()

  # --- set configuration-data   ---------------------------------------------

  def _set_config_data(self):
    """ set configuration. """

    # fix illegal values to defaults
    # channels is pseudo bitfield 001..111 as integer
    if self._settings.ina3221_channels not in CHANNELS:
      self._settings.ina3221_channels = 111
    if self._settings.ina3221_count not in AVG_COUNT:
      self._settings.ina3221_count = 4
    if self._settings.ina3221_ctime < 0 or self._settings.ina3221_ctime > 7:
      self._settings.ina3221_ctime = 2

    # optimize speed vs. noise:
    # measurement-duration is: enabled_channels*count*(v_conv_time+c_conv_time)
    # chip defaults: count=1, conv_time=1.1ms  => 2.2ms*channels
    # lib  defaults: count=64, conv_time=8.244ms => 1055,2ms*channels
    # program defaults: count=4, conv_time=204µs => 1.6ms*channels
    # The resulting sampling time should be shorter than the minimum
    # sampling time of the system. For the EPS32-S2 the minimum is about
    # 5.7ms (serial) or 6.7ms (udp).

    # convert integer channel to binary and activate selected channels
    channels = int(str(self._settings.ina3221_channels),2)
    for index,b in enumerate([0b001,0b010,0b100]):
      self._ina3221[index].enable(bool(b&channels))

    # set averaging count and conversion times
    self._ina3221.averaging_mode = (AVG_COUNT[self._settings.ina3221_count])
    self._ina3221.shunt_voltage_conv_time = CONV_TIME[self._settings.ina3221_ctime]
    self._ina3221.bus_voltage_conv_time = CONV_TIME[self._settings.ina3221_ctime]

  # --- return config-data   -------------------------------------------------

  def get_config_data(self):
    """ return list of tuples (heading,unit,attribute) for configuration """

    return [
      ("Channels","ina3221_channels",""),
      ("AVG-Count","ina3221_count",""),
      ("Conv-Time","ina3221_ctime",""),
      ]

  # --- reset data-provider   ------------------------------------------------

  def reset(self):
    """ reset data-provider """
    self._set_config_data()

  # --- return dimensions of data   ------------------------------------------

  def get_dim(self):
    """ dimension of data """
    return DataProvider._dim

  # --- return units of data   -----------------------------------------------

  def get_units(self):
    """ units of data """
    return DataProvider._units[:DataProvider._dim]

  # --- log-format   ---------------------------------------------------------

  def get_fmt(self):
    """ return format for data, timestamp is {0} """
    return ','.join(DataProvider._fmt[:DataProvider._dim])

  # --- provide data   -------------------------------------------------------

  def get_data(self):
    """ yield the next measurement """

    results = []
    for i in range(3):
      if self._ina3221[i].enabled:
        results.append(self._ina3221[i].bus_voltage)
        results.append(self._ina3221[i].current)
      else:
        results.extend([0,0])
    return results
