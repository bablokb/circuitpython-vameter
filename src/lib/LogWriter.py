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

from Scales import *

class LogWriter:
  """ log data """

  # --- constructor   --------------------------------------------------------

  def __init__(self,app):
    """ constructor """

    self.app = app
    self._fmt = "{0:.1f},"+app.data_provider.get_fmt()+"\n"

  # --- print settings   -----------------------------------------------------

  def log_settings(self):
    """ print settings """

    settings = self.app.settings
    self._int_fac   = int_fac(settings.tm_scale)
    self._dur_scale = dur_scale(settings.tm_scale)
    self._dur_fac   = dur_fac(settings.tm_scale)

    self.log("#\n#Interval:   {0:d}{1:s}\n".format(
      settings.interval,settings.tm_scale))
    if settings.oversample > 0:
      self.log("#Oversampling: {0:d}X\n".format(settings.oversample))
    self.log("#Duration:     {0:d}{1:s}\n".format(
      settings.duration,self._dur_scale))
    self.log("#Update:       {0:d}ms\n#\n".format(settings.update))

  # --- print values   -------------------------------------------------------

  def log_values(self,t,values):
    """ print values """
    self.log(self._fmt.format(1000*t,*values))

  # --- print summary   ------------------------------------------------------

  def log_summary(self,samples):
    """ print summary """

    self.log("#\n#Duration: {0:.1f}{1:s}\n".format(
      self.app.results.time/self._dur_fac,self._dur_scale))
    self.log("#Samples: {0:d} ({1:.1f}/s)\n".format(
      samples,samples/self.app.results.time))
    self.log("#Mean Interval: {0:.1f}{1:s}\n".format(
      self.app.results.time/self._int_fac/samples,
      self.app.settings.tm_scale))
    self.log("#Min,Mean,Max\n")
    units = self.app.data_provider.get_units()
    for index,value in enumerate(self.app.results.values):
      self.log("#{1:.2f}{0:s},{2:.2f}{0:s},{3:.2f}{0:s}\n".format(
        units[index],*value))
