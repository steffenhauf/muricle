# Based on https://randomnerdtutorials.com/esp32-esp8266-micropython-web
# -server/
import uasyncio
try:
    import usocket as socket

    print("Using usocket")
except ImportError:
    import socket

    print("Using socket")

from airquality import AirQuality
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




sensors = [Blinker("Blinker", 2), Barometer("Barometer", 5, 4),
           AirQuality("Air Quality", 0)]


async def serve(reader, writer):

    # read some data
    request = await reader.read(1024)
    # request is in bytes, we decode to a string
    request = request.decode()
    print(f"Request = {request}")

    # check if we should measure
    measure = 'GET /?measure=on' in request

    # note that LED is on on low signal
    measurements = []
    if measure:
        for sensor in sensors:
            pass
            measurements.append(sensor.measure())  # yields a future

    # wait for measurements to actually finish
    await uasyncio.gather(*measurements)

    response = render_page(sensors)
    writer.write('HTTP/1.1 200 OK\n')
    writer.write('Content-Type: text/html\n')
    writer.write(response)
    await writer.drain()
    await writer.wait_closed()


loop = uasyncio.get_event_loop()
loop.create_task(uasyncio.start_server(serve, "0.0.0.0", 80))
try: 
    loop.run_forever()
except KeyboardInterrupt:
    print("closing")
    loop.close()
