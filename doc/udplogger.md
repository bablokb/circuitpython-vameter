Howto use the UDPLogger
=======================

Overview
--------

This class allows data-logging via WLAN on devices with native WIFI.
This is not for devices that have an ESP32 as a coprocessor, e.g. a
PyPortal!

UDP works even if no remote host is listening and thus more robust
than TCP. The setup time (connection to AP) is quite long, but the
overhead during logging is only about 1ms.

To receive the data, run something like

    netcat -u l 6500

on a machine in the network and pass the ip and port of the machine in
the file `secrets.py` (see below).

As an alternative, run

    tools/cp-datalogger.py -t -o mydata.csv

The complete list of options for `cp-datalogger.py` are available via

    tools/cp-datalogger.py -h


Configuration
-------------

Add

    from UDPLogger import DataLogger

to your `user_config.py`.


secrets.py
----------

Create the file `secrets.py` with the following content:

    secrets = {
      'ssid' :        'ssid-of-accesss-point',
      'password' :    'PSK-2 shared key',
      'retry':        number-of-retries,
      'remote_ip':    'IP of remote host receiving the logs',
      'remote_port' : port-number
    }
