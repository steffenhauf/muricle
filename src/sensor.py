class Sensor:

    def __init__(self, name):
        self.name = name

    def measure(self):
        raise NotImplementedError()

    def render(self):
        raise NotImplementedError()
