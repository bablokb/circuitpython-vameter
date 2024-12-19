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

    self._settings = settings
    if not hasattr(self._settings,"ina219_calib"):
      setattr(self._settings,"ina219_calib",1)
    if not hasattr(self._settings,"ina219_adc"):
      setattr(self._settings,"ina219_adc",6)   # ADCResolution.ADCRES_12BIT_8S

    self._ina219 = INA219(i2c)
    self.reset()

  # --- set configuration-data   ---------------------------------------------

  def _set_config_data(self):
    """ set configuration. """

    # voltage and current ranges (resolution increases top-down):
    # everything that is neither 1 or 2 will be interpreted as 16V/400mA!
    # 2: 32V/2A:   488µA
    # 1: 32V/1A:   244µA
    # ?: 16V/400mA: 98µA

    if self._settings.ina219_calib == 2:
      self._ina219.set_calibration_32V_2A()
    elif self._settings.ina219_calib == 1:
      self._ina219.set_calibration_32V_1A()
    else:
      self._ina219.set_calibration_16V_400mA()

    # INA219 oversampling
    # The resulting sampling time should be shorter than the minimum
    # sampling time of the system. For the EPS32-S2 the minimum is about
    # 5.5ms, thus 12BIT_8S (4.26ms) is optimal.

    ADC_RESOLUTION = [
      ADCResolution.ADCRES_9BIT_1S,    #  0
      ADCResolution.ADCRES_10BIT_1S,   #  1
      ADCResolution.ADCRES_11BIT_1S,   #  2
      ADCResolution.ADCRES_12BIT_1S,   #  3
      ADCResolution.ADCRES_12BIT_2S,   #  4
      ADCResolution.ADCRES_12BIT_4S,   #  5
      ADCResolution.ADCRES_12BIT_8S,   #  6
      ADCResolution.ADCRES_12BIT_16S,  #  7
      ADCResolution.ADCRES_12BIT_32S,  #  8
      ADCResolution.ADCRES_12BIT_64S,  #  9
      ADCResolution.ADCRES_12BIT_128S, # 10
      ]

    if self._settings.ina219_adc < 0 or self._settings.ina219_adc > 10:
      self._settings.ina219_adc = 6
    self._ina219.bus_adc_resolution   = ADC_RESOLUTION[self._settings.ina219_adc]
    self._ina219.shunt_adc_resolution = ADC_RESOLUTION[self._settings.ina219_adc]

  # --- return config-data   -------------------------------------------------

  def get_config_data(self):
    """ return list of tuples (heading,unit,attribute) for configuration """

    return [
      ("Calibration","ina219_calib","A"),
      ("ADC-Overs.","ina219_adc",""),
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
