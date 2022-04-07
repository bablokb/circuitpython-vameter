# ----------------------------------------------------------------------------
# Data.py: helper classes for data-collection and aggregation.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
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
    self._data = [[1e6,-1,0] for i in range(self._dim)]

  # --- add data   -----------------------------------------------------------

  def add(self,values):
    """ add data point to aggregation """

    self._n += 1
    for index,value in enumerate(values):
      if index == self._dim:
        break
      self._data[index][1] += value
      if value < self._data[index][0]:
        self._data[index][0] = value
      if value > self._data[index][2]:
        self._data[index][2] = value

  # --- get aggregate values   -----------------------------------------------

  def get(self,index=None):
    """ return aggregate values """

    if index is None:
      return [[data[0],data[1]/self._n,data[2]] for data in self._data]
    else:
      return [self._data[index][0],
              self._data[index][1]/self._n,
              self._data[index][2]]

  # --- get mean values   ----------------------------------------------------

  def get_mean(self):
    """ return mean values """

    return [data[1]/self._n for data in self._data]

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

