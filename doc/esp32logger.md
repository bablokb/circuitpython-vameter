Howto use the ESP32Datalogger
=============================

Overview
--------

This class allows data-logging via WLAN on devices with the ESP32-chip
(e.g. Qt Py ESP32-S2 from Adafruit). This is not for devices that
have an ESP32 as a coprocessor, e.g. a PyPortal!

Compared to the ESP-01, the setup time (connection to AP) is quite long,
but the overhead during logging is only about 1ms.

To receive the data, run something like

    netcat -u l 6500

on a machine in the network and pass the ip and port of the machine in
the file `secrets.py` (see below).


main.py
-------

Import `DataLogger` from `ESP32DataLogger` instead of from `SerialDataLogger`.
You only need to toggle the comment before two lines for that.


secrets.py
----------

Create the file `secrets.py` with the following content:

    secrets = {
      'ssid' :        'ssid-of-accesss-point',
      'password' :    'PSK-2 shared key',
      'transport':    'UDP or TCP',
      'retry':        number-of-retries,
      'remote_ip':    'IP of remote host receiving the logs',
      'remote_port' : port-number
    }

UDP works even if no remote host is listening and is a bit faster.
