# ----------------------------------------------------------------------------
# LogWriter.py: log values
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
#
# ----------------------------------------------------------------------------

class LogWriter:
  """ log data """

  # --- constructor   --------------------------------------------------------

  def __init__(self,app,log_func):
    """ constructor """

    self._app = app
    self._log = log_func
    self._fmt = "{0:.1f},"+app.data_provider.get_fmt()
    if app.settings.tm_scale == 'ms':
      self._tm_scale = 1000
    else:
      self._tm_scale = 1

  # --- print settings   -----------------------------------------------------

  def log_settings(self):
    """ print settings """

    settings = self._app.settings

    self._log("#\n#Interval:   {0:d}{1:s}".format(
      settings.interval,settings.tm_scale))
    if settings.oversample > 0:
      self._log("#Oversampling: {0:d}X".format(settings.oversample))
    self._log("#Duration:     {0:d}s".format(settings.duration))
    self._log("#Update:       {0:d}{1:s}\n#".format(
      settings.update,settings.tm_scale))

  # --- print values   -------------------------------------------------------

  def log_values(self,t,values):
    """ print values """
    self._log(self._fmt.format(1000*t,*values))

  # --- print summary   ------------------------------------------------------

  def log_summary(self,samples):
    """ print summary """

    self._log("#\n#Duration: {0:.1f}s".format(self._app.results.time))
    self._log("#Samples: {0:d} ({1:.1f}/s)".format(
      samples,samples/self._app.results.time))
    self._log("#Interval: {0:.1f}{1:s}".format(
      self._tm_scale*self._app.results.time/samples,
      self._app.settings.tm_scale))
    self._log("#Min,Mean,Max")
    units = self._app.data_provider.get_units()
    for index,value in enumerate(self._app.results.values):
      self._log("#{1:.2f}{0:s},{2:.2f}{0:s},{3:.2f}{0:s}".format(
        units[index],*value))
