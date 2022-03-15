# Getting Started

This page contains a few resources to get started in Micropython development on the ESP8266

First of all, here's the main micropython reference, which will help you in coding: https://docs.micropython.org/en/latest/

The ESP8266 microcontroller, which we are using for this project is described here: https://en.wikipedia.org/wiki/ESP8266

## Setting up a development environment and installing Micropython

For this project we recommend using Thonny-IDE. The following instructions should work on OS X (Mac) and Linux boxes. 
Mostly, follow the instructions at https://randomnerdtutorials.com/getting-started-thonny-micropython-python-ide-esp32-esp8266/, 
if that does not work, you can try `esptool` as discussed at https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html. 
Here we explain a few caveats.

### USB drivers

On MacOs you will likely once neeed to install the USB drivers to be able to flash the ESP8266. Follow the instructions
here: https://cityos-air.readme.io/docs/1-mac-os-usb-drivers-for-nodemcu . On most Linux boxes, this should not
be necessary.

## Sensors, Displays and other hardware addons

### The BMP180 Temperature and Air Pressure Sensor

We are based in Hamburg, and there the weather is sometimes quite nasty. Hence, it's useful to get an early warning on
a decrease in airpressue. The BMP180 can do that for us. It can nicely integrate on the ESP8266 via micropython and the
following library: https://github.com/micropython-IMU/micropython-bmp180
