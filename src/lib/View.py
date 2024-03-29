# ----------------------------------------------------------------------------
# View.py: Various views for the 128x64 oled.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-vameter
#
# ----------------------------------------------------------------------------

import displayio
import terminalio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.sparkline import Sparkline

# --- base class of all Views   ----------------------------------------------

class View:
  FONT_T   = terminalio.FONT
  FONT_S   = bitmap_font.load_font("fonts/DejaVuSansMono-Bold-18-min.pcf")
  FONT_L   = bitmap_font.load_font("fonts/DejaVuSansMono-Bold-32-min.pcf")
  FG_COLOR = 0xFFFFFF

  # --- constructor   --------------------------------------------------------

  def __init__(self,display,border):
    """ constructor """

    self._display = display
    self._border  = 1
    if display:
      self._group   = displayio.Group()
      self._offset = border + 2 if border else 0

      # hack for displays larger than 128x64
      off_w = (display.width-128)/2
      off_h = (display.height-64)/2

      self._pos_map = {
        'NW': ((0.0,0.0),(self._offset+off_w,
                          self._offset+off_h)),
        'NE': ((1.0,0.0),(display.width-self._offset-off_w,
                          self._offset+off_h)),
        'W':  ((0.0,0.5),(self._offset+off_w,
                          display.height/2)),
        'E':  ((1.0,0.5),(display.width-self._offset-off_w,
                          display.height/2)),
        'SW': ((0.0,1.0),(self._offset+off_w,
                          display.height-self._offset-off_h)),
        'SE': ((1.0,1.0),(display.width-self._offset-off_w,
                          display.height-self._offset-off_h)),
        }
      if border:
        rect = Rect(0,0,display.width,display.height,
                    fill=None,outline=View.FG_COLOR,stroke=border)
        self._group.append(rect)

  # --- add a text   ---------------------------------------------------------

  def add(self,text,pos,font):
    """ create and add a label with given text, pos, font """

    if self._display:
      t = label.Label(font,text=text,color=View.FG_COLOR,
                      anchor_point=self._pos_map[pos][0])
      t.anchored_position = self._pos_map[pos][1]
      self._group.append(t)
      return t
    else:
      return None

  # --- format a float   -----------------------------------------------------

  def format(self,value,unit):
    """ format a value """

    if value < 10:
      fmt = "{0:4.2f}{1:s}"
      value = round(value,2)
    elif value < 100:
      fmt = "{0:4.1f}{1:s}"
      value = round(value,1)
    else:
      fmt = "{0:3.0f}{1:s}"
      value = round(value,0)
    return fmt.format(value,unit)

  # --- show the view   ------------------------------------------------------

  def show(self):
    """ show the view """

    if self._display:
      self._display.show(self._group)
      self._display.refresh()

# ----------------------------------------------------------------------------
# --- View for current values   ----------------------------------------------

class ValuesView(View):

  # --- constructor   --------------------------------------------------------

  def __init__(self,display,border,units):
    """ constructor """

    super(ValuesView,self).__init__(display,border)
    if self._display:
      self._value = []
      if len(units) < 3:
        pos  = ['NE','SE']
        font = View.FONT_L
        self._units = units
      else:
        pos  = ['NE','E','SE']
        font = View.FONT_S
        self._units = units[:3]    # we support at most 3 values

      for i,unit in enumerate(self._units):
        self._value.append(self.add(units[i],pos[i],font))

  # --- set values   ---------------------------------------------------------

  def set_values(self,values,elapsed):
    """ set values """

    if self._display:
      for index,value in enumerate(values):
        if index == len(self._value):
          break
        self._value[index].text = self.format(value,self._units[index])

      # TODO: show elapsed time on larger screens

  # --- clear values   -------------------------------------------------------

  def clear_values(self):
    """ clear values """

    if self._display:
      for index in range(len(self._value)):
        self._value[index].text = self._units[index]

  # --- set unit   -----------------------------------------------------------

  def set_units(self,units):
    """ set units for values """

    if self._display:
      self._units = units

# ----------------------------------------------------------------------------
# --- View for results   -----------------------------------------------------

class ResultView(View):

  # --- constructor   --------------------------------------------------------

  def __init__(self,display,border,unit):
    """ constructor """

    super(ResultView,self).__init__(display,border)
    self._unit = unit

    if self._display:
      self._label_min = self.add('min:','NW',View.FONT_S)
      self._value_min = self.add('0.00','NE',View.FONT_S)

      self._label_mean = self.add('mean:','W',View.FONT_S)
      self._value_mean = self.add('0.00','E',View.FONT_S)

      self._label_max = self.add('max:','SW',View.FONT_S)
      self._value_max = self.add('0.00','SE',View.FONT_S)

  # --- set values   ---------------------------------------------------------

  def set_values(self,min,mean,max):
    """ set values for voltage and current """

    if self._display:
      self._value_min.text  = self.format(min,self._unit)
      self._value_mean.text = self.format(mean,self._unit)
      self._value_max.text  = self.format(max,self._unit)

# ----------------------------------------------------------------------------
# --- View for configurations   ----------------------------------------------

class ConfigView(View):

  # --- constructor   --------------------------------------------------------

  def __init__(self,display,border,header,unit):
    """ constructor """

    super(ConfigView,self).__init__(display,border)
    self._unit = unit

    if self._display:
      self._header = self.add(header,'NW',View.FONT_S)
      self._value  = self.add(' ','SE',View.FONT_L)

  # --- set values   ---------------------------------------------------------

  def set_value(self,value):
    """ set value for config-item """

    if self._display:
      self._value.text = "{0:s}{1:s}".format(value,self._unit)

  # --- set unit   -----------------------------------------------------------

  def set_unit(self,unit):
    """ set unit for config-item """

    if self._display:
      self._unit = unit

# ----------------------------------------------------------------------------
# --- PlotView   -------------------------------------------------------------

class PlotView(View):

  # --- constructor   --------------------------------------------------------

  def __init__(self,display,border,units):
    """ constructor (units must be an iterable!) """

    super(PlotView,self).__init__(display,border)
    self._units = units
    self._sparklines = []
    self._values = []
    pos = ['NW','NE']
    for i in range(min(len(units),2)):
      sparkline = Sparkline(
        width=self._display.width-2*self._offset,
        height=self._display.height-2*self._offset,
        max_items=64,
        dyn_xpitch=False,
        x=0, y=0)
      self._sparklines.append(sparkline)
      self._values.append(self.add('0.00',pos[i],View.FONT_T))
      self._group.append(sparkline)

  # --- reset state   --------------------------------------------------------

  def reset(self):
    """ reset state """

    if self._display:
      for sparkline in self._sparklines:
        sparkline.clear_values()

  # --- set values   ---------------------------------------------------------

  def set_values(self,values):
    """ set values (must pass an iterable!) """

    if self._display:
      for i in range(len(self._sparklines)):
        self._sparklines[i].add_value(values[i],update=False)
        self._values[i].text = self.format(values[i],self._units[i])

  # --- show the view   ------------------------------------------------------

  def show(self):
    """ show the view """

    if self._display:
      for i in range(len(self._sparklines)):
        self._sparklines[i].update()
      super(PlotView,self).show()
