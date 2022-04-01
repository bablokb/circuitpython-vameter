# ----------------------------------------------------------------------------
# Data.py: helper classes for data-collection and aggregation.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pico-cp-vameter
#
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# --- Data aggregation helper   ----------------------------------------------

class DataAggregator:
  """ calculate min,mean,max of data """

  # --- constructor   --------------------------------------------------------

  def __init__(self,dim):
    """ constructor """

    self._dim = dim
    self.reset()

  # --- reset data   ---------------------------------------------------------

  def reset(self):
    """ reset data to initial state """

    self._n   = 0
    self._min = [1e6 for i in range(self._dim)]
    self._max = [ -1 for i in range(self._dim)]
    self._sum = [  0 for i in range(self._dim)]

  # --- add data   -----------------------------------------------------------

  def add(self,values):
    """ add data point to aggregation """

    self._n += 1
    for index,value in enumerate(values):
      self._sum[index] += value
      if value < self._min[index]:
        self._min[index] = value
      if value > self._max[index]:
        self._max[index] = value

  # --- get aggregate values   -----------------------------------------------

  def get(self,index=None):
    """ return aggregate values """

    if index is None:
      return (self._min,
              [s/self._n for s in self._sum],
              self._max)
    else:
      return (self._min[index],
              self._sum[index]/self._n,
              self._max[index])

# ----------------------------------------------------------------------------
# --- Data table for plots   -------------------------------------------------

class DataTable:
  """ saves a given number of data-points """

  # --- constructor   --------------------------------------------------------

  def __init__(self,dim,size):
    """ constructor """

    self._dim  = dim
    self._size = size
    self.reset()

  # --- reset data   ---------------------------------------------------------

  def reset(self):
    """ reset data to initial state """

    self._n    = 0
    self._data = [[] for i in range(self._dim)]

  # --- add data   -----------------------------------------------------------

  def add(self,values):
    """ add data point to aggregation """

    # roll data if buffer is full
    if len(self._data[0]) == self._size:
      for i in range(dim):
        self._data[i] = self._data[i][1:]
    # and append new data
    for i in range(dim):
      self._data[i].append(values[i])

  # --- get values   ---------------------------------------------------------

  def get(self,index=None):
    """ return values """

    if index is None:
      return self._data
    else:
      return self._data[index]

