# ----------------------------------------------------------------------------
# View.py: Various views for the 128x64 oled.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pico-cp-vameter
#
# ----------------------------------------------------------------------------

import displayio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect

# --- base class of all Views   ----------------------------------------------

class View:
  FONT_S   = bitmap_font.load_font("fonts/DejaVuSansMono-Bold-18-min.pcf")
  FONT_L   = bitmap_font.load_font("fonts/DejaVuSansMono-Bold-32-min.pcf")
  FG_COLOR = 0xFFFFFF

  # --- constructor   --------------------------------------------------------

  def __init__(self,display,border):
    """ constructor """

    self._display = display
    if display:
      self._group   = displayio.Group()
      offset = border + 2 if border else 0
      self._pos_map = {
        'NW': ((0.0,0.0),(offset,              offset)),
        'NE': ((1.0,0.0),(display.width-offset,offset)),
        'W':  ((0.0,0.5),(offset,              display.height/2)),
        'E':  ((1.0,0.5),(display.width-offset,display.height/2)),
        'SW': ((0.0,1.0),(offset,              display.height-offset)),
        'SE': ((1.0,1.0),(display.width-offset,display.height-offset)),
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

# ----------------------------------------------------------------------------
# --- View for current A/V values   ------------------------------------------

class ValuesView(View):

  # --- constructor   --------------------------------------------------------

  def __init__(self,display,border,units):
    """ constructor """

    super(ValuesView,self).__init__(display,border)
    self._units = units
    if self._display:
      self._value = []
      self._value.append(self.add(units[0],'NE',View.FONT_L))
      self._value.append(self.add(units[1],'SE',View.FONT_L))

  # --- set values   ---------------------------------------------------------

  def set_values(self,values):
    """ set values """

    if self._display:
      for index,value in enumerate(values):
        if index == len(self._value):
          break
        self._value[index].text = self.format(value,self._units[index])

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
      self._value.text = self.format(value,self._unit)
