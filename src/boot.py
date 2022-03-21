# Adapted from
# https://randomnerdtutorials.com/micropython-esp32-esp8266-access-point-ap/

# it's nice to observe alphabetical order here
import gc
import time

import network

# explicitely run gc to free memory
gc.collect()

ssid = 'MicroPython-AP'
password = '123456789'

# setup as accesspoint so we don't require WIFI
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)

# wait til the access point comes up
while not ap.active():
    time.sleep_ms(100)

print('Connection successful')
print(ap.ifconfig())
