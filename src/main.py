# Based on https://randomnerdtutorials.com/esp32-esp8266-micropython-web-server/
import esp
import gc
from machine import Pin
import network
import time
try:
    import usocket as socket
    print("Using usocket")
except:
    import socket
    print("Using socket")
    

def render_page():
    """
    This function is called to render the webserver page
    """
    # we can define variable on outside scope in a conditional experession
    if led.value() == 0:
        gpio_state = "ON"
    else:
        gpio_state = "OFF"

    html = """
<html>
    <head>
        <title>ESP Web Server</title> 
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="icon" href="data:,">
        <style>
            html {
                font-family: Helvetica; 
                display:inline-block; 
                margin: 0px auto; 
                text-align: center;
            }
            h1 {
                color: #0F3376;
                padding: 2vh;
            }
            p {
                font-size: 1.5rem;
            }
            .buttonOn {
                display: inline-block;
                background-color: #e7bd3b; 
                border: none; 
                border-radius: 4px;
                color: white; 
                padding: 16px 40px;
                text-decoration: none; 
                font-size: 30px; 
                margin: 2px; 
                cursor: pointer;
            }
            .buttonOff {
                background-color: #4286f4;
            }
        </style>
    </head>
    <body>
        <h1>ESP Web Server</h1> 
        <p>GPIO state: <strong>""" + gpio_state + """</strong></p>
        <p>
            <a href="/?led=on">
                <button class="buttonOn">ON</button>
            </a>
        </p>
        <p>
            <a href="/?led=off">
                <button class="buttonOn buttonOff">OFF</button>
            </a>
        </p>
    </body>
</html>
"""
    return html


# setup a socket to listen on port 80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

print("Bound to port 80")

while True:
    # wait on a new connection
    conn, addr = s.accept()
    # f-strings allow to include formatted vars into strings
    print(f"Got a connection from {addr}")
    # read some data
    request = conn.recv(1024)
    # request is in bytes, we decode to a string
    request = request.decode()
    print(f"Request = {request}")
    
    # check if either led on or off was requested
    led_on = 'GET /?led=on' in request
    led_off = 'GET /?led=off' in request
    
    # note that LED is on on low signal
    if led_on:
        print('LED ON')
        led.value(0)
    if led_off:
        print('LED OFF')
        led.value(1)
    
    response = render_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
