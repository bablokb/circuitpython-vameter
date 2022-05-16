# ----------------------------------------------------------------------------
# SerialLogger.py: log values to the serial console
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
#
# ----------------------------------------------------------------------------

class DataLogger:
  """ log data to the serial console """

  # --- constructor   --------------------------------------------------------

  def __init__(self,app):
    """ constructor """

    self._app = app
    self._fmt = "{0:.1f},"+app.data_provider.get_fmt()

  # --- print settings   -----------------------------------------------------

  def log_settings(self):
    """ print settings """

    settings = self._app.settings

    print("\n#Interval:   {0:d}ms".format(settings.interval))
    if settings.oversample > 0:
      print("#Oversampling: {0:d}X".format(settings.oversample))
    print("#Duration:     {0:d}s".format(settings.duration))
    print("#Update:       {0:d}ms\n".format(settings.update))

  # --- print values   -------------------------------------------------------

  def log_values(self,t,values):
    """ print values """
    print(self._fmt.format(1000*t,*values))

  # --- print summary   ------------------------------------------------------

  def log_summary(self,samples):
    """ print summary """

    print("\n#Duration: {0:.1f}s".format(self._app.results.time))
    print("#Samples: {0:d} ({1:.1f}/s)".format(samples,
                                               samples/self._app.results.time))
    print("#Interval: {0:.0f}ms".format(1000*self._app.results.time/samples))
    print("#Min,Mean,Max")
    units = self._app.data_provider.get_units()
    for index,value in enumerate(self._app.results.values):
      print("#{1:.2f}{0:s},{2:.2f}{0:s},{3:.2f}{0:s}".format(units[index],*value))
