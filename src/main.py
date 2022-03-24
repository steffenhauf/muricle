# Based on https://randomnerdtutorials.com/esp32-esp8266-micropython-web
# -server/
try:
    import usocket as socket

    print("Using usocket")
except ImportError:
    import socket

    print("Using socket")

from barometer import Barometer
from blinker import Blinker


def render_page(sensors):
    """
    This function is called to render the webserver page
    """
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
            .button {
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

            .sensor {
                border: 1px solid black;
            }

        </style>
    </head>
    <body>
        <h1>ESP Web Server</h1>

        <p>
            <a href="/?measure=on">
                <button class="button">MEASURE</button>
            </a>
        </p>
"""
    for sensor in sensors:
        html += """
        <div class="sensor">
            <p>""" + sensor.name + "</p>" + sensor.render() + """
        </div>
        """
    html += """
    </body>
</html>
"""
    return html


# setup a socket to listen on port 80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

print("Bound to port 80")

sensors = [Blinker("Blinker", 2), Barometer("Barometer", 5, 4),]

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

    # check if we should measure
    measure = 'GET /?measure=on' in request

    # note that LED is on on low signal
    if measure:
        for sensor in sensors:
            sensor.measure()

    response = render_page(sensors)
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
