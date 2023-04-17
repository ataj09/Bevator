from time import sleep

import pigpio


class Motor:
    def __init__(self):
        self.endswich1_pin = 1
        self.endswich2_pin = 2
        self.pumps_pin = [3, 4, 5, 6]

        self.pi = pigpio.pi()

        self.pi.set_mode(self.endswich1_pin, pigpio.INPUT)
        self.pi.set_mode(self.endswich2_pin, pigpio.INPUT)

        for i in self.pumps_pin:
            self.pi.set_mode(i, pigpio.OUTPUT)

    def loop(self):
        pass

    def run_pump(self, no, time):
        self.pi.write(self.pumps_pin[no], pigpio.HIGH)
        sleep(time)
