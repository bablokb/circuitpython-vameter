Project circuitpython-vameter
=============================


Overview
--------

This repository contains the necessary CircuitPyhon software to drive a
voltage/current meter based on the following components:

  - INA219 current-sensor breakout
  - Mini OLED display with 128x64 (based on a SSD1306-chip) or
  - SPI TFT-1.8" display (based on a ST7735R-chip)
  - 4x3 touchpad (based on a MPR121-chip)

Measurements are shown on the display and written as CSV to the
console.

Note that the display and touchpad are not strictly necessary. In
this case (i.e. you only want to measure voltage/current)
you have to change configuration values directly within the source-code.

If you want to use other components (especially a bigger display or
knobs and buttons instead of the touchpad) you should read the
[hacking guide](doc/hacking.md).


Hardware
--------

All components use I2C except if you choose to use the SPI-display.
Connect the respective SDA, SCL, Vcc and GND
pins with the relevant pins of the MCU. Don't forget pullups, the builtin
pullups of the MCU are usually too weak.

![](doc/hardware.jpg)

On the left edge: the MCU, a RP2040-Qt-Trinkey. The INA219 is left to the
barrel-jack on the upper-left side of the breadboard. On the top edge
of the image is a load-resistor. In real applications this resistor is
replaced by the load you want to measure.

The mini-oled with 128x64 pixels is in the middle, on the right is a
MPR121-based keypad with 12 keys. A template for the key-mapping is in
`doc/keypad-template.png` and `doc/keypad-template.odg`.
The latter also has a version for horizontal orientation but in this case
you have to change the mapping code in `src/lib/Touchpad.py` as well.

The INA219-breakout has two pins (next to the I2C-interface) and a
screw-terminal for attachement of the power-source (V+) and the load (V-).
**Don't use the pins, use the screw-terminal** or else your results will
be off by about 20%.


Installation (Pico or other MCU)
--------------------------------

Steps:

  0. Install the current version of CircuitPython to your device

  1. Install the following libraries from the CircuitPython library-bundle to
     the `lib`-directory of your device

    - adafruit_bitmap_font
    - adafruit_displayio_ssd1306
    - adafruit_st7735r
    - adafruit_display_shapes
    - adafruit_display_text
    - adafruit_ina219
    - adafruit_register
    - adafruit_mpr121

    The preferred way to do this is to use `circup` (note that the device
    must be mounted):

        sudo apt-get -y install pip3
        sudo pip3 install circup
        circup install -r requirements.txt

  2. Clone the repository

  3. If you are using a MCU which does not define board-pins for SDA and
     SCL etc. (e.g. Raspberry Pi Pico): change the pin-values in `src/main.py`.
     The SPI-display needs additional pins, these are also defined there.

  4. Check `src/lib/INA219DataProvider.py` for the correct voltage range.
     The code uses the library-default of 32V/2A, but this can be changed
     to 16V/1A or 16V/400mA. The additional precision is probably not
     worth the effort. Also, you can change the chip-internal oversampling
     of the ADC. The Default uses 8x oversampling resulting in a minimal
     sampling time of 4.26ms.

  5. Copy all files from below `src` to your device.


Installation (Raspberry Pi)
---------------------------

There is a native build of CircuitPython for the Raspberry Pi, but that
build is extremely slow and not usable yet. The better option is to
use _Blinka_, an emulation layer which provides classes and methods usually
missing in a native python installation. Blinka runs on various SBCs,
the Raspberry Pi is only the most prominent example.

You can install the project on a Raspberry Pi (or any other Debian-based SBC
with Blinka-support) using:

    sudo tools/install-pi

This installs the project files, Blinka and all necessary libraries to
`/usr/local/cp-vameter`. To run the program, just use the command
`cp-vameter`. This assumes that `/usr/local/bin` is within your path.

Note that the installation is quite slow, because the install-command
installs everything to a python-virtenv. Especially download, compile
and install of numpy takes a lot of time, even on the faster Pis. For
running the program, a Pi-Zero is more than sufficient.

Also note that Blinka currently only supports SPI-displays with 16-bit
colors.

Usage
-----

The program is in three modes: _ready_ (after power-on and reset),
_active_ and _config_. Possible transitions are _ready-active-ready_ and
_ready-config-ready_.

To switch modes, use the keypad:

![](doc/keyboard-template.png)

Keys in blue are valid for the ready-mode, keys in black during configuration
and keys in red during the active-mode.


Ready-Mode
----------

The ready-mode displays the last measurement-results (switch by using the
"View"-button):

![](doc/result-view-v.png) ![](doc/result-view-a.png)

Use the "Start" or "Config"-buttons to start a measurement or to enter
configuration mode.


Config-Mode
-----------

Once the program is in configuration mode, you can enter various parameters:

  - **Interval**: the sampling interval in milliseconds  
    ![](doc/config-int-view.png)
  - **Duration**: the duration of the measurement in seconds. A value of zero
    will run the measurement until it is explicitly or implicitly stopped.  
    ![](doc/config-dur-view.png)
  - **Update**: update-interval of the screen in milliseconds. These updates
    slow down the sampling, so make sure this value is much larger than the
    value of `interval`. Setting the value to zero will disable
    updates of the display during measurement.  
    ![](doc/config-upd-view.png)

The "Next"-button will navigate through the configuration screens, after the
last item the system switches back to ready-mode.


Active-Mode
-----------

During active-mode the program continuously reads the sensor and collects
and displays data. Actual sampling starts as soon as the voltage and
current is above a default threshold (1V/0.5mA) and stops again once

  - the values drop again below these limits, or
  - the configured measurement duration is reached or
  - you press the "Stop"-button

Using the "View"-button you cycle through various views:

  - voltage and current  
    ![](doc/values-view.png)
  - elapsed time  
    ![](doc/elapsed-view.png)
  - plot-view of voltage  
    ![](doc/plot-view-v.png)
  - plot-view of current  
    ![](doc/plot-view-a.png)


Tips and Tricks
---------------

The default configuration of the sensor uses 8x oversampling for the
internal ADC. This reduces noise. Sampling-time according to the
datasheet is 4.26ms. Using less oversampling or less precision you
can bring this down to below 1ms, but if you really need high-frequency
sampling in this range you should think about reimplementing the project
using an optimzed setup and probably C/C++.

Using a Pico, you can reach a minimal sampling interval of about 8ms
(6ms measured on a Pi3B+).

Display-updates take about 330ms. During update, you loose all samples.
Setting the update-interval to zero prevents data-loss. When the
sampling-interval is larger than 330ms, no data-loss occurs regardless
of display-updates.

For ex-post data-visualization, save the data from the serial output
to a file, remove comment-lines and then use the
[Python Datamonitor](https://github.com/bablokb/py-datamon) to create
a plot. A ready to use configuration-file is in
[doc/cp-vameter.json](./cp-vameter.json).

The INA219 provides voltage, current and power. The default configuration
does not sample power. If you need all three values, you can change
this within `lib/INA219DataProvider` (set `WITH_POWER=True`).

In this file you can also change some additional settings, e.g. sample
frequency and voltage/current range as well as the cutoff-values used
for detecting start and stop of measurements.
