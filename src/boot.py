# Complete project details at https://RandomNerdTutorials.com
# Adapted from https://randomnerdtutorials.com/micropython-esp32-esp8266-access-point-ap/

try:
  import usocket as socket
except:
  import socket

import network

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'MicroPython-AP'
password = '123456789'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)

while ap.active() == False:
  pass

print('Connection successful')
print(ap.ifconfig())
led = Pin(2, Pin.OUT)
