# ----------------------------------------------------------------------------
# BlinkaExtensions.py: extensions when running on a SBC
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
#
# ----------------------------------------------------------------------------

from argparse import ArgumentParser

# --- update settings from cmdline-args   ------------------------------------

def update_settings(settings):
  """ update settings from cmdline arguments """

  parser = _get_parser(settings)
  parser.parse_args(namespace=settings)

# --- create parser   --------------------------------------------------------

def _get_parser(settings):
  """ create parser """

  parser = ArgumentParser(prog="cp-vameter",
                          add_help=False,
                          description='cp-vameter - sample sensor-data')

  parser.add_argument('-i', '--interval', metavar='interval',
      default=settings.interval, type=int,
      help='sampling interval')
  parser.add_argument('-s', '--scale', metavar='scale',
      default=settings.int_scale, type=str, dest='int_scale',
      help='time-scale (ms or s)')
  parser.add_argument('-o', '--oversample', metavar='oversample',
      default=settings.oversample, type=int,
      help='oversampling')
  parser.add_argument('-D', '--duration', metavar='duration',
      default=settings.duration, type=int,
      help='duration of measurement')
  parser.add_argument('-u', '--update', metavar='update',
      default=settings.update, type=int,
      help='screen update interval')
  parser.add_argument('-n', '--no-plots', action='store_false',
      dest='plots', default=settings.plots,
      help="disable plots")
  parser.add_argument('-e', '--exit', action='store_true',
      dest='exit', default=settings.exit,
      help="exit after measurement")
  parser.add_argument('-h', '--help', action='help',
      help='print this help')

  return parser
