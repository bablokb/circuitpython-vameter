Project circuitpython-vameter
=============================


Overview
--------

This repository contains the necessary CircuitPyhon software to drive a
voltage/current meter based on the following components:

  - INA219 breakout
  - Mini OLED display with 128x64 (based on a SSD1306-chip)
  - 4x3 touchpad (based on a MPR121-chip)

Measurements are shown on the display and written as CSV to the
console.

Note that the display and touchpad are not strictly necessary. In
this case (i.e. you only want to measure voltage/current)
you have to change configuration values directly within the source-code.

If you want to use other components (especially a bigger display or
knobs and buttons instead of the touchpad) you should read the
[porting guide](doc/porting.md).


Hardware
--------

All components use I2C. Connect the respective SDA, SCL, Vcc and GND
pins with the relevant pins of the MCU. Don't forget pullups, the builtin
pullups of the MCU are usually too weak.

![](doc/hardware.jpg)

On the left edge: the MCU, a RP2040-Qt-Trinkey. The INA219 is left to the
barrel-jack on the upper-left side of the breadboard.

The INA219-breakout has two pins (next to the I2C-interface) and a
screw-terminal for attachement of the power-source (V+) and the load (V-).
*Don't use the pins, use the screw-terminal* or else your results will
be off by about 20%.


Installation
------------

Steps:

  1. Clone the repository

  2. Add the following libraries from the CircuitPython library-bundle to
     `src/lib`

    - adafruit_bitmap_font
    - adafruit_displayio_ssd1306
    - adafruit_display_shapes
    - adafruit_display_text
    - adafruit_ina219
    - adafruit_register
    - adafruit_mpr121

  3. if you are using a MCU which does not define board-pins for SDA and
     SCL (e.g. Raspberry Pi Pico): change the pin-values in `src/main.py`.

  4. copy all files from `src` to your device.


Usage
-----

To be written.
