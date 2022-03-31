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
  FONT_S   = bitmap_font.load_font("fonts/DejaVuSansMono-Bold-18-min.bdf")
  FONT_L   = bitmap_font.load_font("fonts/DejaVuSansMono-Bold-32-min.bdf")
  FG_COLOR = 0xFFFFFF

  # --- constructor   --------------------------------------------------------

  def __init__(self,display,border):
    """ constructor """

    self._display = display
    self._group   = displayio.Group()
    offset = border + 2 if border else 0
    self._pos_map = {
      'NW': ((0.0,0.0),(offset,              offset)),
      'NE': ((1.0,0.0),(display.width-offset,offset)),
      'W':  ((0.0,0.5),(offset,              display.height/2)),
      'E':  ((0.5,0.5),(display.width-offset,display.height/2)),
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

    t = label.Label(font,text=text,color=View.FG_COLOR,
                    anchor_point=self._pos_map[pos][0])
    t.anchored_position = self._pos_map[pos][1]
    self._group.append(t)
    return t

  # --- show the view   ------------------------------------------------------

  def show(self):
    """ show the view """

    self._display.show(self._group)

# --- View for current A/V values   ------------------------------------------

class ValuesView(View):

  # --- constructor   --------------------------------------------------------

  def __init__(self,display,border):
    """ constructor """

    super(ValuesView,self).__init__(display,border)
    self._value_V = self.add('0.00V','NE',View.FONT_L)
    self._value_A = self.add('0.00mA','SE',View.FONT_L)

  # --- set values   ---------------------------------------------------------

  def set_values(self,v,a):
    """ set values for voltage and current """

    if a < 10:
      fmt = "{0:4.2f}mA"
      a = round(a,2)
    elif a < 100:
      fmt = "{0:4.1f}mA"
      a = round(a,1)
    else:
      fmt = "{0:3.0f}mA"
      a = round(a,0)

    self._value_V.text = "{0:4.2f}V".format(v)
    self._value_A.text = fmt.format(a)
