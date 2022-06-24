# ----------------------------------------------------------------------------
# ActiveState.py: Handle active-state, i.e. display current values
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
#
# ----------------------------------------------------------------------------

import time
import sys
import asyncio
from View import ValuesView, PlotView
from Data import DataAggregator
from Scales import *

class ActiveState:
  """ manage active-state """

  # --- constructor   --------------------------------------------------------

  def __init__(self,app):
    """ constructor """

    self._app      = app
    self._settings = app.settings
    self._logger   = app.logger
    self._int_fac = int_fac(app.settings.tm_scale)
    self._dur_fac = dur_fac(app.settings.tm_scale)
    self._dim      = app.data_provider.get_dim()

    self._stop       = False    # global stop for all tasks
    self._new_sample = False    # toggle after each sample

    if self._app.display:
      self._cur_view = 0
      d_scale     = dur_scale(app.settings.tm_scale)
      self._views = [ValuesView(app.display,app.border,
                                 app.data_provider.get_units()),
                      ValuesView(app.display,app.border,
                                 [d_scale,d_scale])]  # elapsed
      if self._settings.plots:
        for unit in app.data_provider.get_units():
          self._views.append(PlotView(app.display,app.border,[unit]))

  # --- get data   -----------------------------------------------------------

  def _get_data(self):
    """ get data using oversampling """

    if self._settings.oversample < 2:
      return (time.monotonic(),self._app.data_provider.get_data())

    d_sum = [0 for i in range(self._dim)]
    for o in range(self._settings.oversample):
      data = self._app.data_provider.get_data()
      for i in range(self._dim):
        d_sum[i] += data[i]
    return (time.monotonic(),
            [d_sum[i]/self._settings.oversample for i in range(self._dim)])

  # --- check for key-press   ------------------------------------------------

  async def _check_key(self):
    """ check for key and save it """

    if not self._app.key_events:
      return

    while not self._stop:
      key = self._app.key_events.is_key_pressed(
                                           self._app.key_events.KEYMAP_ACTIVE)
      if key == 'TOGGLE' and self._app.display:
        # switch to next view
        self._cur_view = (self._cur_view+1) % len(self._views)
      elif key == 'STOP':
        self._stop = True
        return
      await asyncio.sleep(0.1)

  # --- update views   -------------------------------------------------------

  def _update_views(self):
    """ update views """

    if self._app.display and self._settings.update:
      if self._new_sample and self._settings.plots:
        # update plots
        #s =  time.monotonic()
        for i,value in enumerate(self.data_v):
          self._views[2+i].set_values([value])
        #print("#display plots: %f" % (time.monotonic()-s))
      #s =  time.monotonic()
      if self._new_sample and self._cur_view == 0:
        # measurement values
        self._views[self._cur_view].set_values(
          self.data_v,time.monotonic()-self._start_t)
      elif self._cur_view == 1:
        # elapsed time
        self._views[self._cur_view].set_values(
          [(time.monotonic()-self._start_t)/self._dur_fac,
           self._settings.duration],-1)
      #print("#display values: %f" % (time.monotonic()-s))

  # --- show current views   -------------------------------------------------

  async def _show_view(self):
    """ show current view """

    if not (self._app.display and self._settings.update):
      return

    update_time = 0.33                                  # pico,SSD1306
    while not self._stop:
      await asyncio.sleep(self._settings.update/1000)
      gap = self._next_sample_t - time.monotonic()

      # don't start update just before next sample, unless sampling-interval
      # is smaller than update-time (in the latter case we miss samples
      # anyhow)
      if gap < update_time and update_time < self._int_t:
        # wait with update after the next sample
        await asyncio.sleep(gap+0.01)

      # update display with current values
      s = time.monotonic()
      self._update_views()
      if self._new_sample or not self._app.key_events or self._cur_view == 1:
        self._views[self._cur_view].show()
        update_time = time.monotonic() - s
        #print("#_show_view: %f" % update_time)

      self._new_sample = False
      if not self._app.key_events:                      # auto toggle view
        self._cur_view = (self._cur_view+1) % len(self._views)


  # --- loop during ready-state   --------------------------------------------

  def run(self):
    """ main-loop during active-state """

    self._stop     = False
    asyncio.run(self._run())

  # --- loop during ready-state   --------------------------------------------

  async def _run(self):
    """ main-loop during active-state """

    self._int_t = self._settings.interval*self._int_fac # interval time in sec

    key_task  = asyncio.create_task(self._check_key())
    view_task = asyncio.create_task(self._show_view())

    self._logger.log_settings()
    m_data = DataAggregator(self._dim)
    c_view = 0
    if self._app.display:
      if self._settings.plots:
        # reset plots and show first ValuesView
        for i in range(self._dim):
          self._views[2+i].reset()
      self._views[0].clear_values()
      self._views[0].show()

    # reset data-provider and wait for first sample
    self._app.data_provider.reset()
    try:
      self._app.data_provider.get_data()
    except:
      print("\n#data-provider timed out")
      return

    if self._settings.duration:
      end_t = time.monotonic() + self._settings.duration*self._dur_fac
    else:
      end_t = sys.maxsize

    data_t0 = 0                                      # timestamp before last sample
    self._start_t = time.monotonic()                 # timestamp of start
    samples = 0                                      # total number of samples

    # sample until manual stop or until end of duration
    while not self._stop and time.monotonic() < end_t:

      # sleep until next sampling interval starts (int_t minus overhead)
      if data_t0 > 0:
        sleep_t = max(self._int_t-(time.monotonic()-data_t0),0)
        self._next_sample_t = time.monotonic() + sleep_t
        if sleep_t:
          await asyncio.sleep(sleep_t)

      # get, log and save data
      try:
        data_t0 = time.monotonic()
        self.data_t,self.data_v = self._get_data()
        self._new_sample = True
        self._logger.log_values(self.data_t,self.data_v)
        #s =  time.monotonic()
        m_data.add(self.data_v)
        #print("#add: %f" % (time.monotonic()-s))
        samples += 1
      except StopIteration:
        self._stop = True
        break

      if self._stop:
        break

    # that's it, save and log results
    self._app.results.time    = self.data_t - self._start_t
    self._app.results.samples = samples
    self._app.results.values  = m_data.get()

    self._logger.log_summary(samples)

    self._stop = True
    await asyncio.gather(key_task,view_task)
