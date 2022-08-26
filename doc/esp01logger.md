Howto use the ESP01Datalogger
=============================

Overview
--------

This class allows data-logging via WLAN. The ESP-01S is a cheap and
simple MCU. For this application you need the default AT-firmware of
the ESP-01.

Logging via WLAN adds an overhead of 103-115ms, so this is not suitable
for high frequency sampling.

To receive the data, run something like

    netcat -u l 6500

on a machine in the network and pass the ip and port of the machine in
the file `secrets.py` (see below).


Wiring
------

Connect RX, TX from the Pico with TX, RX on the device. Additionally connect
3V3 and GND. If the Pico does not supply enough current, connect an
AMS1117 (or a similar 5V->3V3 regulator) to the VBUS-pin of the Pico and feed
the ESP-01S from the output of the regulator.


Configuration
-------------

Add

    import DataLogger from ESP01DataLogger

to your `user_config.py`.

Check the pin-configuration for `PIN_RX` and `PIN_TX`. Most MCUs will
provide this from `board`, but the Pico is very flexible so you will have
to adjust the defaults to your needs (also within `user_config.py`).


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
