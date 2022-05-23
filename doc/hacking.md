Porting to other hardware
=========================

Since CircuitPython runs on a wide array of platforms, this is not so
much about porting the code to something totally different, but to adapt
it for other hardware components.

This document gives an overview over the application classes to help
changing the code for other hardware. All files are relative to `src`, after
installation relative to the root of the device.


main.py
-------

Here you define pin-numbers and import classes. When implementing new
versions, keep the class name and change the import statement. The class
`FakeDataProvider` vs. `INA219DataProvider` is an example.

The file also defines a number of global constants. This is useful for
setups e.g. without a touchpad.

lib/View.py
-----------

This file defines all the views for the application. To adapt to larger
displays, add colors and so on you have to provide your own implementation.

The small 128x64 display is fine for up to three rows of data. The plot-view
is already more of a gimmick. Better, but still afordable are
160x128 TFT-displays (attached to SPI). The current support of this
display is minimal, the code only uses the central 128x64 pixels and
ignores the availability of colors.

The fonts in the `fonts`-directory are stripped down versions of the
original fonts. If you need additional characters, follow the instructions
in [fonts.md](./fonts.md).


lib/Touchpad.py
---------------

This file implements the class `KeyEventProvider`. For other hardware like
buttons and rotary-encoders, implement a class with identical methods.

An interessting platform would be the PyPortal-line. It has an integrated
processor and with the touch-display you could implement an onscreen
touchpad.


lib/INA219DataProvider.py
-------------------------

The file implements the class `DataProvider`. You could swap the dataprovider
with something simlar (e.g. INA260) or totally different. A BME280 sensor with
temperature, pressure and humidity would be a candidate.

An alternative implementation which is part of the project is the
`FakeDataProvider.py`. It is useful during development and testing since it
does neither need a real current-sensor, nor an existing load.

Other sensors would certainly need other characters within the font-set,
so you must also update the fonts.

If the data-provider is not targeted at sampling in the milliseconds realm,
you should also change the constant `DEF_TM_SCALE` to `s` instead of `ms` in
`main.py`.


lib/SerialLogger.py
-------------------

Implements the class `DataLogger` (logging to the serial console).
Alternative implementations must implement at least the `log()`-method.


lib/ESP01Logger.py
-------------------

Implements the class `DataLogger` (logging via WLAN). For details, read
the [ESP-01 logging HowTo](./esp01logger.md).
