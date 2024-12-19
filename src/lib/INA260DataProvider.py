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
    if not hasattr(self._settings,"ina260_count"):
      setattr(self._settings,"ina260_count",16)
    if not hasattr(self._settings,"ina260_ctime"):
      setattr(self._settings,"ina260_ctime",1)      # ConversionTime.TIME_204_us

    self._ina260 = INA260(i2c)
    self.reset()

  # --- set configuration-data   ---------------------------------------------

  def _set_config_data(self):
    """ set configuration. """

    # fix illegal values to defaults
    if not hasattr(AveragingCount,f"COUNT_{self._settings.ina260_count}"):
      self._settings.ina260_count = 16
    if self._settings.ina260_ctime < 0 or self._settings.ina260_ctime > 7:
      self._settings.ina260_ctime = 1

    # optimize speed vs. noise:
    # measurement-duration is count*(v_conf_time+c_conv_time)
    # chip defaults: 2.2ms
    # program defaults: count=16, conf_time=202µs => 6.5ms
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
    self._ina260.averaging_count = (
      getattr(AveragingCount,f"COUNT_{self._settings.ina260_count}"))

    # conversion time for measurement
    CONV_TIME = [
      ConversionTime.TIME_140_us,     # 0
      ConversionTime.TIME_204_us,     # 1
      ConversionTime.TIME_332_us,     # 2
      ConversionTime.TIME_588_us,     # 3
      ConversionTime.TIME_1_1_ms,     # 4
      ConversionTime.TIME_2_116_ms,   # 5
      ConversionTime.TIME_4_156_ms,   # 6
      ConversionTime.TIME_8_244_ms,   # 7
      ]
    self._ina260.current_conversion_time = CONV_TIME[self._settings.ina260_ctime]
    self._ina260.voltage_conversion_time = CONV_TIME[self._settings.ina260_ctime]

  # --- return config-data   -------------------------------------------------

  def get_config_data(self):
    """ return list of tuples (heading,unit,attribute) for configuration """

    return [
      ("AVG-Count","ina260_count",""),
      ("Conv-Time","ina260_ctime",""),
      ]

  # --- reset data-provider   ------------------------------------------------

  def reset(self):
    """ reset data-provider """
    self._start = False
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
