Project circuitpython-vameter
=============================

**Note: this is work-in-progress and not usable yet**

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
[porting guide](porting.md).


Hardware
--------

All components use I2C. Connect the respective SDA, SCL, Vcc and GND
pins with the relevant pins of the MCU.


Installation
------------

Steps:

  1. Clone the repository

  2. Add the following libraries from the CircuitPython library-bundle to
`    src/lib`:
    - adafruit_bitmap_font
    - adafruit_displayio_ssd1306
    - adafruit_display_shapes
    - adafruit_display_text
    - adafruit_ina219
    - adafruit_mpr121

  3. if you are using a MCU which does not define board-pins for SDA and
     SCL (e.g. Raspberry Pi Pico): change the pin-values in `src/main.py`.

  4. copy all files from `src` to your device.


Usage
-----

To be written.
