# ----------------------------------------------------------------------------
# Scales.py: scale-factors for interval and duration
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
#
# ----------------------------------------------------------------------------

import collections

# map interval-scale to (factor,duration-scale)

INT_SCALES = collections.OrderedDict([
  ('ms', (0.001,'s')),
  ('s',  (1.0,  'm')),
  ('m',  (60.0, 'h')),
  ('h',  (3600.0, 'd')),
  ('d',  (86400.0, 'd'))
  ])

# return factors and scale-labels

def int_fac(scale):
  """ return interval-factor for given scale """
  return INT_SCALES[scale][0]

def dur_scale(scale):
  """ return duration-scale for given int-scale """
  return INT_SCALES[scale][1]

def dur_fac(scale):
  """ return duration-factor for given int-scale """
  return INT_SCALES[dur_scale(scale)][0]
