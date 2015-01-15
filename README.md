Strobe Alert
============

This was a hackday project in January 2015 at Facebook.  The intent was to create a device which would alert engineers when a server or service failure was ongoing.  Really the intent was to create an annoying box that we could put on our manager's desk so that he could share the pain of operational issues with the engineers.  

This repo contains the end result of that project.  We made a physical enclosure, drew a fritzing circuit diagram, wired up a mosfet, arduino, button, power, etc.  Wrote the arduino C code to receive serial commands, a python client application on the other end of the serial communication, and finally a server web process running on the correct side of a corporate firewall that could determine if there were engineering operational alerts present.

Bill of Materials
=================

- Arduino:          https://www.adafruit.com/products/50 - $25
- Big Dome button:  https://www.sparkfun.com/products/9181 - $10
- Mosfet breakout:  https://www.sparkfun.com/products/10256 - $4
- Strobe light:     http://www.amazon.com/Huoshang-Security-Alarm-Strobe-System/dp/B00IIFHAPC - $8
- USB Cable:        https://www.sparkfun.com/products/512 - $4
- Diode:            https://www.sparkfun.com/products/10926 - $0.15


Software Requirements
=====================
For the complete package you will need:
- Arduino development environment: http://arduino.cc/en/main/software
- Python 2.7
- PySerial: https://pypi.python.org/pypi/pyserial
- Fritzing: http://fritzing.org/home/
