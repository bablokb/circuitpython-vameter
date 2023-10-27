# ----------------------------------------------------------------------------
# INA219DataProvider.py: query data from INA219 (I2C-Chip)
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
#
# ----------------------------------------------------------------------------    
#     ADCRES_9BIT_1S = 0x00     #  9bit,   1 sample,     84us
#     ADCRES_10BIT_1S = 0x01    # 10bit,   1 sample,    148us
#     ADCRES_11BIT_1S = 0x02    # 11 bit,  1 sample,    276us
#     ADCRES_12BIT_1S = 0x03    # 12 bit,  1 sample,    532us
#     ADCRES_12BIT_2S = 0x09    # 12 bit,  2 samples,  1.06ms
#     ADCRES_12BIT_4S = 0x0A    # 12 bit,  4 samples,  2.13ms
#     ADCRES_12BIT_8S = 0x0B    # 12bit,   8 samples,  4.26ms
#     ADCRES_12BIT_16S = 0x0C   # 12bit,  16 samples,  8.51ms
#     ADCRES_12BIT_32S = 0x0D   # 12bit,  32 samples, 17.02ms
#     ADCRES_12BIT_64S = 0x0E   # 12bit,  64 samples, 34.05ms
#     ADCRES_12BIT_128S = 0x0F  # 12bit, 128 samples, 68.10ms
# ----------------------------------------------------------------------------

import time
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219

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

    if not hasattr(settings,'v_min'):
      settings.v_min = 1.0                # set default threshold to 1V
    if not hasattr(settings,'a_min'):
      settings.a_min = 0                  # set default threshold to 0mA
    self._settings = settings
    self._ina219   = INA219(i2c)
    self.reset()

    # voltage and current ranges (resolution increases top-down):
    # 32V/2A:   488µA
    # 16V/1A:   244µA
    # 16V/400mA: 98µA
    # library default
    self._ina219.set_calibration_32V_2A()     # ADCResolution.ADCRES_12BIT_1S
    #self._ina219.set_calibration_16V_1A()    # ADCResolution.ADCRES_12BIT_1S
    #self._ina219.set_calibration_16V_400mA() # ADCResolution.ADCRES_12BIT_1S

    # INA219 oversampling, see table above
    # The resulting sampling time should be shorter than the minimum
    # sampling time of the system. For the EPS32-S2 the minimum is about
    # 5.5ms, thus 12BIT_8S (4.26ms) is optimal.
    # For faster MCUs, you need to change this
    self._ina219.bus_adc_resolution   = ADCResolution.ADCRES_12BIT_8S
    self._ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_8S

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
      v = self._ina219.bus_voltage     # voltage on V- (load side)
      a = max(0,self._ina219.current)  # current in mA
      p = self._ina219.power

      if self._ina219.overflow:
        continue

      if v >= self._settings.v_min and a >= self._settings.a_min:
        self._start = True
        return (v,a,1000*p) if WITH_POWER else (v,a)
      elif self._start:
        # voltage dropped below threshold, so we stop
        raise StopIteration
      elif time.monotonic() - t_start > NO_LOAD_TIMEOUT:
        raise StopIteration
