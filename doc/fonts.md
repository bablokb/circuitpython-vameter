Fonts
=====

The program uses the *DejaVuSansMono-Bold* font in three different
font-sizes for the SSD1306 display.

To keep the size small, only the subset of characters actually used
are within the font. These subsets were created following the
tutorial from
<https://learn.adafruit.com/custom-fonts-for-pyportal-circuitpython-display>.

Conversion to PCF was done using the online converter from
<https://adafruit.github.io/web-bdftopcf/>.

Text strings
------------

The program uses the following text strings:

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
  - ms
  - mW
  - s

Character table
---------------

| Char | Tiny | Small | Large |
|------|------|-------|-------|
| sp   |   X  |   X   |   X   |
| .    |   X  |   X   |   X   |
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
| U    |      |   X   |       |
| V    |   X  |   X   |   X   |
| W    |   X  |   X   |       |
| a    |      |   X   |       |
| d    |      |   X   |       |
| e    |      |   X   |       |
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

