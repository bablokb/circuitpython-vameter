Fonts
=====

The program uses the *DejaVuSansMono-Bold* font in two different
font-sizes. The tiny-font is the default builtin font `terminalio.FONT`. If
you prefer a different tiny-font, change the definition within
'src/lib/View.py`.

To keep the size small, only the subset of characters actually used
are within the fonts. These subsets were created following the
tutorial from
<https://learn.adafruit.com/custom-fonts-for-pyportal-circuitpython-display>.

Conversion to PCF was done using the online converter from
<https://adafruit.github.io/web-bdftopcf/>.

Text strings
------------

The program uses the following text strings:

  - Int-Scale:
  - Interval:
  - Oversample:
  - Duration:
  - Update:
  - min:
  - mean:
  - max:


Values and Units
----------------

Characters needed for values and units:

  - numbers
  - V
  - mA
  - mW
  - ms, s, m, h, d


Character table
---------------

Note that the tiny-version if the font currently contains all characters
unless you change the definition. In this case ensure that all characters
from the table are contained in the font.


| Char | Tiny | Small | Large |
|------|------|-------|-------|
| sp   |   X  |   X   |   X   |
| .    |   X  |   X   |   X   |
| -    |      |   X   |       |
| 0    |   X  |   X   |   X   |
| 1    |   X  |   X   |   X   |
| 2    |   X  |   X   |   X   |
| 3    |   X  |   X   |   X   |
| 4    |   X  |   X   |   X   |
| 5    |   X  |   X   |   X   |
| 6    |   X  |   X   |   X   |
| 7    |   X  |   X   |   X   |
| 8    |   X  |   X   |   X   |
| 9    |   X  |   X   |   X   |
| :    |   X  |   X   |   X   |
| A    |   X  |   X   |   X   |
| D    |      |   X   |       |
| I    |      |   X   |       |
| M    |   X  |   X   |   X   |
| O    |      |   X   |       |
| S    |      |   X   |       |
| U    |      |   X   |       |
| V    |   X  |   X   |   X   |
| W    |   X  |   X   |       |
| a    |      |   X   |       |
| c    |      |   X   |       |
| d    |      |   X   |   X   |
| e    |      |   X   |       |
| h    |      |   X   |   X   |
| i    |      |   X   |       |
| l    |      |   X   |       |
| m    |   X  |   X   |   X   |
| n    |      |   X   |       |
| o    |      |   X   |       |
| p    |      |   X   |       |
| r    |      |   X   |       |
| s    |   X  |   X   |   X   |
| t    |      |   X   |       |
| u    |      |   X   |       |
| v    |      |   X   |       |
| x    |      |   X   |       |
|------|------|-------|-------|

