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
    self._data = pd.read_csv(infile,header=None,sep=',')

    # add column labels
    if len(self._data.columns) == 3:
      self._data.columns = ['ts','V','I']
    else:
      # we have a second timestamp at the end
      self._data.columns = ['ts','V','I','ts_iso']
      
  # --- normalize data   -----------------------------------------------------

  def _normalize(self):

    self._data['ts']    -= self._data['ts'][0]
    self._data['ts']    *= 0.001
    self._data['P']      = self._data['I']*self._data['V']

  # --- calcuate statistics   -------------------------------------------------

  def _calc_stats(self):
    """ calculate statistics """

    # calculate cumulative sum of energy-consumption
    t = self._data['ts']   # shortcut to ts-column
    self._esum  = (t.diff()*self._data['P']).cumsum()

    self._stats = {
      'duration': t.max(),
      'A': {'min': float(self._data['I'].min()),
            'avg': float(self._data['I'].mean()),
            'max': float(self._data['I'].max())
            },
      'V': {'min': float(self._data['V'].min()),
            'avg': float(self._data['V'].mean()),
            'max': float(self._data['V'].max())
            },
      'P': {'min': float(self._data['P'].min()),
            'avg': float(self._data['P'].mean()),
            'max': float(self._data['P'].max())
            },
      'E': self._esum.max()/3600 
      }

  # --- print results   -------------------------------------------------------

  def _print_txt(self):
    """ print summary results """
    
    print("\nmeasurement-duration: %5.1f sec" % self._stats['duration'])

    print("\n--------------------------------")
    for attr,label,unit in [
      ('A','current','mA'),('V','voltage','V'),('P','power','mW')]:
      for stat in ['min','avg','max']:
        print("  {0:s} {1:s} {2:6.3f} {3:s}".format(stat,label,
                                                    self._stats[attr][stat],unit))
    print("  tot energy %6.3f mWh" % self._stats['E'])
    print("----------------------------\n")

  # --- dump results as json   ------------------------------------------------

  def _print_json(self):
    """ print results in json-format """

    json.dump(self._stats,sys.stdout,indent=2)

  # --- dump results as csv   -------------------------------------------------

  def _print_csv(self):
    """ print summary results in csv-format"""

    print("#duration,A_min,A_avg,A_max,V_min,V_avg,V_max,P_min,P_avg,P_max,E")
    print("{0:5.1f}".format(self._stats['duration']),end='')

    for attr in ['A','V','P']:
      for stat in ['min','avg','max']:
        print(",{0:6.3f}".format(self._stats[attr][stat]),end='')
    print(",{0:6.3f}".format(self._stats['E']),end='')

    print()

  # --- create csv with cumsum-data   ----------------------------------------

  def _create_csv(self):
    """ create new csv with added cumsum-data """

    # append to data
    self._data['E_SUM'] = self._esum

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
