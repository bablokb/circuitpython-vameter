#!/usr/bin/python3
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------
# Read data from UDP/serial and preprocess (filter, add timestamp)
#
# UDP has no prereqs and should run fine on any platform
# If you want to use the serial interface, you need to install pyserial.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
#
# --------------------------------------------------------------------------

import locale, os, sys, threading, signal, datetime, time
import socket
from   argparse import ArgumentParser

try:
  import serial
  have_serial = True
except:
  have_serial = False

# --- application class   ----------------------------------------------------

class Reader(object):

  MSG_LENGTH    = 80         # total message-length
  MSG_COLUMNS   =  3         # colums per message 
  V_MIN         = 0.05       # default filter-limit for voltage in V
  PORT          = 6500       # default UDP-port
  NET           = "0.0.0.0"  # default UDP-net
  TIMEOUT_START = 60         # initial timeout for socket
  TIMEOUT       = 10         # timeout for socket

  # if serial is available and used
  SERIAL_BAUD   = '/dev/ttyACM0,115200'     # serial-line,baud-rate

  # all column-numbers are zero-based
  COL_V       =  1         # column input voltage
  
  # --- constructor   --------------------------------------------------------

  def __init__(self):
    """ constructor """

    self._stop_event = threading.Event()
    self._file       = None
    self._success    = 0
    self._incomplete = 0
    self._filtered   = 0
    self._failed     = 0

    parser = self._get_parser()
    parser.parse_args(namespace=self)
    if not have_serial:
      self.serial_baud = None

    if self.serial_baud:
      self.tty,self.baud = self.serial_baud.split(',')
      self.baud = int(self.baud)
      
  # --- cmdline-parser   -----------------------------------------------------

  def _get_parser(self):
    """ configure cmdline-parser """

    parser = ArgumentParser(add_help=False,
                            description='CP-VAMeter UDP-Datareader')

    parser.add_argument('-p', '--port', metavar='port',
      default=Reader.PORT, type=int,
      help='UDP-port to listen to (default: %d)' % Reader.PORT)
    parser.add_argument('-i', '--ip-net', metavar='net',
      dest='net', default=Reader.NET,
      help='network to listen to (default: %s)' % Reader.NET)
    if have_serial:
      parser.add_argument('-s', '--serial', metavar='tty,baudrate',
        dest='serial_baud', default=None, const=Reader.SERIAL_BAUD, nargs='?',
        help='use serial instead of UDP (default : %s)' % Reader.SERIAL_BAUD)

    parser.add_argument('-V', '--volt-filter', metavar='volt',
      dest='volt', type=int, default=Reader.V_MIN,
      help='lower filter-limit for voltage (mV, default: %d)' % Reader.V_MIN)
    parser.add_argument('-D', '--duration', metavar='duration',
      dest='duration', type=int, default=None,
      help='limit measurment to given duration in seconds (default: no limit)')

    parser.add_argument('-t', '--time-stamp', metavar='ts-format',
      dest='ts_format', default=None, const='i', nargs='?',
      help="add additional column with timestamp (u=unix, i=iso or generic format")

    parser.add_argument('-o', '--output', metavar='outfile',
      dest='outfile',default=None,help='save data to outfile')
    parser.add_argument('-a', '--append', action='store_true',
      dest='append', default=False,help='append data (needs option -o)')
    parser.add_argument('-n', '--no-stdout', action='store_true',
      dest='no_stdout', default=False,
      help="don't write data to stdout (needs option -o)")

    parser.add_argument('-d', '--debug', action='store_true',
      dest='debug', default=False,
      help="force debug-mode")
    parser.add_argument('-q', '--quiet', action='store_true',
      dest='quiet', default=False,
      help="don't print messages")
    parser.add_argument('-h', '--help', action='help',
      help='print this help')

    return parser

  # --- print message   ------------------------------------------------------

  def msg(self,text,force=False):
    """ print message """

    if force and not self.quiet:
      sys.stderr.write("%s\n" % text)
    elif self.debug:
      sys.stderr.write("[DEBUG %s] %s\n" % (time.strftime("%H:%M:%S"),text))
    sys.stderr.flush()

  # --- setup signal handler   ------------------------------------------------

  def signal_handler(self,_signo, _stack_frame):
    """ signal-handler for clean shutdown """

    self.msg("Reader: received signal, stopping program ...")
    self._stop_event.set()

  # --- cleanup ressources   -------------------------------------------------

  def cleanup(self):
    """ cleanup ressources """

    if self._file:
      self._file.flush()
      self._file.close()

  # --- run application   ----------------------------------------------------

  def run(self):
    """ run application """

    # setup signal-handler
    signal.signal(signal.SIGTERM, self.signal_handler)
    signal.signal(signal.SIGINT,  self.signal_handler)

    # start main loop
    self.msg("Reader: running...")
    if self._process_input():

      # some stats
      self.msg("\nProtocol\n========\n",force=True)
      self.msg("Start:    %s" % self._start_dt.strftime("%x %X"),force=True)
      self.msg("End:      %s" % self._end_dt.strftime("%x %X"),force=True)
      self.msg("Duration: %s\n" % self._pp_time(),force=True)

      total = self._success + self._filtered + self._failed + self._incomplete
      if total:
        self.msg("Messages:",force=True)
        self.msg("  total:      %d" % total,force=True)
        self.msg("  success:    %d" % self._success,force=True)
        self.msg("  filtered:   %d" % self._filtered,force=True)
        self.msg("  failed:     %d" % self._failed,force=True)
        self.msg("  incomplete: %d" % self._incomplete,force=True)
        self.msg("  interval:   %5.3f ms" % (1000*self._ttime/total),force=True)

    # and bye
    self.cleanup()
    sys.exit(0)

  # --- pretty print duration/time   ----------------------------------------

  def _pp_time(self):
    """ pritty-print time as mm:ss or hh:mm """

    m, s = divmod(int(self._ttime),60)
    h, m = divmod(m,60)
    if h > 0:
      return "{0:02d}:{1:02d}:{2:02d}".format(h,m,s)
    else:
      return "{0:02d}:{1:02d}".format(m,s)

  # --- process input   ------------------------------------------------------

  def _process_input(self):
    """ read input, process and output """

    if self.outfile:
      if self.append:
        fmt = 'a'
      else:
        fmt = 'w'
      try:
        self._file = open(self.outfile,fmt)
      except Exception as ex:
        self.msg("could not open %s" % self.outfile,force=True)
        self.msg("error: %s" % ex,force=True)
        sys.exit(3)

    if self.serial_baud:
      self.msg("Reader: serial-interface: reading from %s (%d)" %
               (self.tty,self.baud))
      try:
        tty = serial.Serial(self.tty,self.baud)
        tty.timeout = Reader.TIMEOUT
        if tty.isOpen():
          tty.close()
        tty.open()
      except Exception as ex:
        self.msg("error: could not open serial-line",force=True)
        self.msg("error: %s" % ex,force=True)
        sys.exit(3)
    else:
      self.msg("Reader: UDP-interface: reading from port %d (%s)" %
               (self.port,self.net))
      # create UDP
      sock = socket.socket(socket.AF_INET, # Internet
                           socket.SOCK_DGRAM) # UDP
      sock.bind((self.net,self.port))
      sock.settimeout(Reader.TIMEOUT_START)

    # note that this is not (yet) a robust implementation, because sp3 sends
    # three packages and we might just start in the middle.
    first = True
    start = sys.float_info.max
    buffer = ""
    while True:
      # check for interruption
      if self._stop_event.is_set():
        self.msg("Reader: request to stop reading")
        if self.serial_baud:
          tty.close()
        break

      # read data
      self.msg("Reader: buffer: %r" % buffer)
      ind_nl = buffer.find("\n")
      if ind_nl > 0:
        msg    = buffer[:ind_nl]
        buffer = buffer[ind_nl+1:]
        self.msg("Reader:   msg: %r" % msg)
        self.msg("Reader:   buf: %r" % buffer)
      else:
        if self.serial_baud:
          data = tty.read(size=Reader.MSG_LENGTH)
          if len(data) == 0:
            self.msg("\nerror: serial timeout after %ds" % Reader.TIMEOUT,force=True)
            tty.close()
            break
          else:
            buffer = "".join([buffer,data.decode("utf-8",errors='ignore')])
            continue
        else:
          try:
            data, _ = sock.recvfrom(Reader.MSG_LENGTH)
            # take some timings for the report
            self._ttime = time.perf_counter()-start
            self._end_dt = datetime.datetime.now()
            buffer = "".join([buffer,data.decode("utf-8",errors='ignore')])
            continue
          except socket.timeout:
            if first:
              self.msg("\nerror: socket timeout after %ds" %
                       Reader.TIMEOUT_START,force=True)
              return False
            else:
              self.msg("\nsocket timeout after %ds" % Reader.TIMEOUT)
            break

      #pstart = time.perf_counter()
      success = self._process_msg(msg)
      if first and success:
        # take some timings for the report at start
        self._start_dt = datetime.datetime.now()
        start = time.perf_counter()
        sock.settimeout(Reader.TIMEOUT)
        first = False
      #print("elapsed: %f" % (time.perf_counter()-pstart),file=sys.stderr)

      #exit if measurement duration is reached
      if self.duration and time.perf_counter()-start > self.duration:
        break

    return True

  # --- process single message   ---------------------------------------------

  def _process_msg(self,data):
    """ process a single message """

    if data[0] == "#":
      # pass comment without change
      value = data
    else:
      words = data.split(',')
      if len(words) != Reader.MSG_COLUMNS:
        self.msg("Reader: ignoring incomplete message: %s" % data)
        self._incomplete += 1
        return False
      if self.volt:
        try:
          if self._filter(words):
            self._filtered += 1
            return False
        except Exception as ex:
          self._failed += 1
          self.msg("Reader: failed message: %s" % data)
          self.msg("Reader: exception: %s" % ex)
          return False

      self._success += 1
      if self.ts_format:
        if self.ts_format == 'u':
          value = '{},{}'.format(data,datetime.datetime.now().timestamp())
        elif self.ts_format == 'i':
          value = '{},"{}"'.format(data,datetime.datetime.now().isoformat())
        else:
          value = '{},"{}"'.format(data,
                                   datetime.datetime.now().strftime(self.ts_format))
      else:
        value = data

    # output data to stdout and to file
    if not self.no_stdout:
      print(value,flush=True)
    if self._file:
      print(value,file=self._file)

    return data[0] == '#'

  # --- filter the given message   -------------------------------------------

  def _filter(self,data):
    """ filter the given data: returns True if filtering is necessary """

    if self.volt:
      if (float(data[Reader.COL_V]) < self.volt):
        self.msg("Reader: discarding message (voltage): %r" % (data,))
        return True

    return False
    
# --- main program   ---------------------------------------------------------

if __name__ == '__main__':

  # set local to default from environment
  locale.setlocale(locale.LC_ALL, '')

  # create client-class and parse arguments
  reader = Reader()
  reader.run()
  signal.pause()
  reader.cleanup()
