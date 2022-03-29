from machine import I2C, Pin

from mq135 import MQ135
from sensor import Sensor


class AirQuality(Sensor):

    def __init__(self, name, analogue_pin, temperature=21.0, humidity=25.0):
        super().__init__(name)
        self.temperature = temperature
        self.humidity = humidity
        self.mq135 = MQ135(analogue_pin)
        self.rzero = 0
        self.corrected_rzero = 0
        self.resistance = 0
        self.ppm = 0
        self.corrected_ppm = 0
        self.measure()

    async def measure(self):
        self.rzero = f"{self.mq135.get_rzero():0.2f}"
        self.corrected_rzero = f"{self.mq135.get_corrected_rzero(self.temperature, self.humidity):0.2f}"
        self.resistance = f"{self.mq135.get_resistance():0.2f}"
        self.ppm = f"{self.mq135.get_ppm():0.2f}"
        self.corrected_ppm = f"{self.mq135.get_corrected_ppm(self.temperature, self.humidity):0.2f}"

    def render(self):

        html = """
        <p>rzero: <strong>""" + self.rzero + """</strong></p>
        <p>corr. rzero: <strong>""" + self.corrected_rzero + """</strong></p>
        <p>resistance: <strong>""" + self.resistance + """ Ohm</strong></p>
        <p>ppm: <strong>""" + self.ppm + """</strong></p>
        <p>corr. ppm: <strong>""" + self.corrected_ppm + """</strong></p>
        """
        return html
