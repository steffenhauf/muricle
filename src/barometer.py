from machine import I2C, Pin

from bmp180 import BMP180
from sensor import Sensor


class Barometer(Sensor):

    def __init__(self, name, scl_pin, sda_pin,
                 pressure_baseline=101325,
                 altitude_adjust=0):
        super().__init__(name)
        # for ESP8266
        bus = I2C(scl=Pin(scl_pin), sda=Pin(sda_pin), freq=100000)
        self.bmp180 = BMP180(bus)
        self.bmp180.oversample_sett = 3
        self.bmp180.baseline = pressure_baseline
        self.altitude_adjust = altitude_adjust
        self.p = 0
        self.altitude = 0
        self.temp = 0
        self.measure()

    async def measure(self):
        self.bmp180.blocking_read()

    def render(self):
        temp = f"{self.bmp180.temperature:0.2f}"
        p = f"{self.bmp180.pressure/100:0.2f}"
        altitude = f"{self.bmp180.altitude + self.altitude_adjust:0.2f}"

        html = """
        <p>Pressure: <strong>""" + p + """ hPa</strong></p>
        <p>Altitude: <strong>""" + altitude + """ m</strong></p>
        <p>Temperature: <strong>""" + temp + """ &#8451;</strong></p>

        """
        return html
    
    def get_values(self):
        values = {"temp": self.bmp180.temperature,
                  "pressure": self.bmp180.pressure/100,
                  "altitude": self.bmp180.altitude}
        return values
