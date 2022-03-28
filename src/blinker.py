import uasyncio
from machine import Pin

from sensor import Sensor


class Blinker(Sensor):

    def __init__(self, name, pin, blink_duration=5):
        super().__init__(name)

        # we will need the LED pin later for some blinking.
        self.led = Pin(pin, Pin.OUT)
        self.blink_duration = blink_duration

    async def measure(self):
        # turns on the led
        self.led.value(0)
        loop = uasyncio.get_event_loop()
        loop.create_task(self._reset_blink())

    def render(self):
        status = "OFF" if self.led.value() == 1 else "ON"
        html = """
        <p>LED is: <strong>""" + status + """ </strong></p>
        """
        return html

    async def _reset_blink(self):
        print("blinking")
        await uasyncio.sleep(self.blink_duration)
        # turns off the led
        self.led.value(1)