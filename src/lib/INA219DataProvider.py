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

class DataProvider:
  """ provide data """

  # --- constructor   --------------------------------------------------------

  def __init__(self,i2c,settings):
    """ constructor """

    if not hasattr(settings,'v_min'):
      settings.v_min = 1.0                # set default threshold to 1V
    self._settings = settings
    self._ina219   = INA219(i2c)
    self.reset()

    # INA219 oversampling, see table above
    self._ina219.bus_adc_resolution   = ADCResolution.ADCRES_12BIT_8S
    self._ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_8S

    # voltage and current ranges (resolution increases top-down)
    self._ina219.set_calibration_32V_2A()         # library default
    #self._ina219.set_calibration_16V_1A()
    #self._ina219.set_calibration_16V_400mA()

  # --- reset data-provider   ------------------------------------------------

  def reset(self):
    """ reset data-provider """
    self._start = False

  # --- return dimensions of data   ------------------------------------------

  def get_dim(self):
    """ dimension of data """
    return 2

  # --- return units of data   -----------------------------------------------

  def get_units(self):
    """ units of data """
    return ['V','mA']

  # --- log-format   ---------------------------------------------------------

  def get_fmt(self):
    """ return format for data, must include placeholder for timestamp """
    return "{0:.1f},{1:.2f},{2:.1f}"

  # --- provide data   -------------------------------------------------------

  def get_data(self):
    """ yield the next measurement """

    # Loop until voltage is above threshold.
    # The loop degenerates as long as the voltage is high enough.
    while True:
      v = self._ina219.bus_voltage  # voltage on V- (load side)
      a = self._ina219.current      # current in mA

      if v > self._settings.v_min:
        self._start = True
        return (v,a)
      elif self._start:
        # voltage dropped below threshold, so we stop
        raise StopIteration
