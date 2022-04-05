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
max_attempts = 20
while not ap.active() and max_attempts > 0:
    time.sleep_ms(100)
    max_attempts -= 1

if max_attempts > 0:
    print('Connection successful')
    print(ap.ifconfig())
else:
    print("Coundn't connect to WIFI")
