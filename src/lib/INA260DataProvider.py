# ----------------------------------------------------------------------------
# INA260DataProvider.py: query data from INA260 (I2C-Chip)
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
# ----------------------------------------------------------------------------

import time
from adafruit_ina260 import ConversionTime, AveragingCount, INA260

WITH_POWER      = False  # normally False, set to True to add power-attribute
NO_LOAD_TIMEOUT = 60     # timeout (sec) if there is no load for given duration

class DataProvider:
  """ provide data """

  _dim   = 3 if WITH_POWER else 2
  _units = ['V','mA','mW']
  _fmt   = ["{1:.3f}","{2:.3f}","{3:.3f}"]

  # --- constructor   --------------------------------------------------------

  def __init__(self,i2c,settings):
    """ constructor """

    self._settings = settings
    self._ina260   = INA260(i2c)

    # optimize speed vs. noise:
    # measurement-duration is count*(v_conf_time+c_conv_time)
    # chip defaults: 2.2ms
    # program defaults: 6.5ms
    # The resulting sampling time should be shorter than the minimum
    # sampling time of the system. For the EPS32-S2 the minimum is about
    # 5.7ms (serial) or 6.7ms (udp).

    # rolling averaging:
    # COUNT_1
    # COUNT_4
    # COUNT_16
    # COUNT_64
    # COUNT_128
    # COUNT_256
    # COUNT_512
    # COUNT_1024
    #self._ina260.averaging_count = AveragingCount.COUNT_1
    self._ina260.averaging_count = AveragingCount.COUNT_16

    # conversion time for measurement
    # TIME_140_us
    # TIME_204_us
    # TIME_332_us
    # TIME_588_us
    # TIME_1_1_ms
    # TIME_2_116_ms
    # TIME_4_156_ms
    # TIME_8_244_ms
    #self._ina260.current_conversion_time = ConversionTime.TIME_1_1_ms
    self._ina260.current_conversion_time = ConversionTime.TIME_204_us
    self._ina260.voltage_conversion_time = ConversionTime.TIME_204_us

    self.reset()

  # --- reset data-provider   ------------------------------------------------

  def reset(self):
    """ reset data-provider """
    self._start = False

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

    # Loop until voltage is above threshold.
    # The loop degenerates as long as the voltage is high enough.
    t_start = time.monotonic()
    while True:
      v = self._ina260.voltage
      a = max(0,self._ina260.current)  # current in mA
      p = self._ina260.power

      if v >= self._settings.v_min and a >= self._settings.a_min:
        self._start = True
        return (v,a,1000*p) if WITH_POWER else (v,a)
      elif self._start:
        # voltage dropped below threshold, so we stop
        raise StopIteration
      elif time.monotonic() - t_start > NO_LOAD_TIMEOUT:
        raise StopIteration
