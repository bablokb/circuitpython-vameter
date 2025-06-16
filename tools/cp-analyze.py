#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------
# Analyse data.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
#
# --------------------------------------------------------------------------

import sys, locale, json
from   argparse import ArgumentParser

import pathlib
import pandas as pd

COLUMN_HEADERS = [
  None, None, None,
  ['ts','V1','I1'],                               # for INA219 and INA260
  ['ts','V1','I1','ts_iso'],
  None, None,
  ['ts','V1','I1','V2','I2','V3','I3'],           # for INA3221
  ['ts','V1','I1','V2','I2','V3','I3','ts_iso'],
  ]

# --- application class   ----------------------------------------------------

class App(object):

  # --- constructor   --------------------------------------------------------

  def __init__(self):
    """ constructor """

    parser = self._get_parser()
    parser.parse_args(namespace=self)

  # --- cmdline-parser   -----------------------------------------------------

  def _get_parser(self):
    """ configure cmdline-parser """

    parser = ArgumentParser(add_help=False,description='cp-vameter data analysis')

    parser.add_argument('-o', '--output-format', dest='otype', default='txt',
                      metavar='output-format',
                      choices=['txt','csv','json'],
           help="output-format of summary (one of 'txt','csv','json')")

    parser.add_argument('-c', '--cumulative', metavar='cumsum.csv',
                        dest='cumsum_file', default=None,
                        help='create new csv with cumulative sum of energy')
    parser.add_argument('-r', '--relative', action='store_true',
      dest='relative', default=False,
      help="create additional column with relative cumulative sum of energy")
    parser.add_argument('-C', '--comments', action='store_true',
      dest='comments', default=False,
      help="assume comments starting with #")

    parser.add_argument('-d', '--debug', action='store_true',
      dest='debug', default=False,
      help="force debug-mode")
    parser.add_argument('-q', '--quiet', action='store_true',
      dest='quiet', default=False,
      help="don't print messages")
    parser.add_argument('-h', '--help', action='help',
      help='print this help')

    parser.add_argument('input', metavar='input', help='input-file')

    return parser

  # --- read data   ----------------------------------------------------------

  def _read_data(self):
    """ read data and prepare dataframe """

    infile = self.input
    if self.comments:
      self._data = pd.read_csv(infile,header=None,sep=',',comment='#')
    else:
      self._data = pd.read_csv(infile,header=None,sep=',')

    # add column labels
    self._data.columns = COLUMN_HEADERS[len(self._data.columns)]
    self._channels = 3 if len(self._data.columns) > 4 else 1
      
  # --- normalize data   -----------------------------------------------------

  def _normalize(self):

    self._data['ts']    -= self._data['ts'][0]
    self._data['ts']    *= 0.001
    for i in range(1,self._channels+1):
      self._data[f'P{i}'] = self._data[f'I{i}']*self._data[f'V{i}']

  # --- calcuate statistics   -------------------------------------------------

  def _calc_stats(self):
    """ calculate statistics """

    # calculate cumulative sum of energy-consumption
    t = self._data['ts']   # shortcut to ts-column
    self._esum = [None]
    for i in range(1,self._channels+1):
      self._esum.append((t.diff()*self._data[f'P{i}']).cumsum())

    self._stats = {
      'duration': t.max()
    }
    for i in range(1,self._channels+1):
      self._stats.update({
        f'A{i}': {'min': float(self._data[f'I{i}'].min()),
                  'avg': float(self._data[f'I{i}'].mean()),
                  'max': float(self._data[f'I{i}'].max())
                 },
        f'V{i}': {'min': float(self._data[f'V{i}'].min()),
                  'avg': float(self._data[f'V{i}'].mean()),
                  'max': float(self._data[f'V{i}'].max())
                 },
        f'P{i}': {'min': float(self._data[f'P{i}'].min()),
                  'avg': float(self._data[f'P{i}'].mean()),
                  'max': float(self._data[f'P{i}'].max())
                 },
        f'E{i}': self._esum[i].max()/3600
      })

  # --- print results   -------------------------------------------------------

  def _print_txt(self):
    """ print summary results """
    
    print("\nmeasurement-duration: %5.1f sec" % self._stats['duration'])

    print("\n--------------------------------\n")
    for i in range(1,self._channels+1):
      print(f"Channel {i}:")
      for attr,label,unit in [
        (f'A{i}','current','mA'),(f'V{i}','voltage','V'),(f'P{i}','power','mW')]:
        for stat in ['min','avg','max']:
          print("  {0:s} {1:s} {2:6.3f} {3:s}".format(stat,label,
                                                      self._stats[attr][stat],unit))
      print("  tot energy %6.3f mWh" % self._stats[f'E{i}'])
      print("----------------------------\n")

  # --- dump results as json   ------------------------------------------------

  def _print_json(self):
    """ print results in json-format """

    json.dump(self._stats,sys.stdout,indent=2)

  # --- dump results as csv   -------------------------------------------------

  def _print_csv(self):
    """ print summary results in csv-format"""

    # csv-header
    print("#duration",end="")
    for i in range(1,self._channels+1):
      print(f",A{i}_min,A{i}_avg,A{i}_max", end="")
      print(f",V{i}_min,V{i}_avg,V{i}_max", end="")
      print(f",P{i}_min,P{i}_avg,P{i}_max,E{i}", end="")
    print()

    # csv-values
    print("{0:5.1f}".format(self._stats['duration']),end='')
    for i in range(1,self._channels+1):
      for attr in [f'A{i}',f'V{i}',f'P{i}']:
        for stat in ['min','avg','max']:
          print(",{0:6.3f}".format(self._stats[attr][stat]),end='')
      print(",{0:6.3f}".format(self._stats[f'E{i}']),end='')
    print()

  # --- create csv with cumsum-data   ----------------------------------------

  def _create_csv(self):
    """ create new csv with added cumsum-data """

    # append to data
    for i in range(1,self._channels+1):
      self._data[f'E_SUM{i}'] = self._esum[i]

      if self.relative:
        max_esum = self._stats[f'E{i}']*3600
        self._data[f'E_SUM_R{i}'] = self._esum[i]/max_esum

    # write to new csv
    outfile = pathlib.Path(self.cumsum_file)
    self._data.to_csv(outfile,index=False)

  # --- run application   ----------------------------------------------------

  def run(self):
    """ run application """

    self._read_data()
    self._normalize()

    self._calc_stats()
    if self.otype == 'txt':
      self._print_txt()
    elif self.otype == 'json':
      self._print_json()
    else:
      self._print_csv()

    if self.cumsum_file:
      self._create_csv()

# --- main program   ---------------------------------------------------------

if __name__ == '__main__':

  # set local to default from environment
  locale.setlocale(locale.LC_ALL, '')

  # create client-class and parse arguments
  app = App()
  app.run()
