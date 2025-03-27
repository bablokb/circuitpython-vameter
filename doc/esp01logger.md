Howto use the ESP01Datalogger
=============================

Support for the ESP-01S has been dropped. The code used the library
`adafruit_espat` which is no longer supported.

Nevertheless, logging with WIFI using an ESP-01S still works. To use
it, you need to install the library
[circuitpython-esp32at](https://github.com/bablokb/circuit-python-esp32at). Once
installed, initialize the wifi-coprocessor in your `user_config.py`. After
initialization, use the standard [UDPLogger](./udplogger.md) for
logging.
