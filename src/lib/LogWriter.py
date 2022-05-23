# ----------------------------------------------------------------------------
# LogWriter.py: log values
#
# Subclasses have to implement the method log(string)
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

  def __init__(self,app):
    """ constructor """

    self.app = app
    self._fmt = "{0:.1f},"+app.data_provider.get_fmt()
    if app.settings.tm_scale == 'ms':
      self._tm_scale = 1000
    else:
      self._tm_scale = 1

  # --- print settings   -----------------------------------------------------

  def log_settings(self):
    """ print settings """

    settings = self.app.settings

    self.log("#\n#Interval:   {0:d}{1:s}".format(
      settings.interval,settings.tm_scale))
    if settings.oversample > 0:
      self.log("#Oversampling: {0:d}X".format(settings.oversample))
    self.log("#Duration:     {0:d}s".format(settings.duration))
    self.log("#Update:       {0:d}{1:s}\n#".format(
      settings.update,settings.tm_scale))

  # --- print values   -------------------------------------------------------

  def log_values(self,t,values):
    """ print values """
    self.log(self._fmt.format(1000*t,*values))

  # --- print summary   ------------------------------------------------------

  def log_summary(self,samples):
    """ print summary """

    self.log("#\n#Duration: {0:.1f}s".format(self.app.results.time))
    self.log("#Samples: {0:d} ({1:.1f}/s)".format(
      samples,samples/self.app.results.time))
    self.log("#Interval: {0:.1f}{1:s}".format(
      self._tm_scale*self.app.results.time/samples,
      self.app.settings.tm_scale))
    self.log("#Min,Mean,Max")
    units = self.app.data_provider.get_units()
    for index,value in enumerate(self.app.results.values):
      self.log("#{1:.2f}{0:s},{2:.2f}{0:s},{3:.2f}{0:s}".format(
        units[index],*value))
