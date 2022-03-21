from machine import Pin

from sensor import Sensor


class Blinker(Sensor):

    def __init__(self, name, pin):
        super().__init__(name)

        # we will need the LED pin later for some blinking.
        self.led = Pin(pin, Pin.OUT)

    def measure(self):
        if self.led.value() == 0:
            self.led.value(1)
        else:
            self.led.value(0)

    def render(self):
        status = "OFF" if self.led.value() == 1 else "ON"
        html = """
        <p>LED is: <strong>""" + status + """ </strong></p>
        """
        return html
