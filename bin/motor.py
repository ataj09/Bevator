from time import sleep

import pigpio
import time

class Motor:
    def __init__(self):
        """
        Equivalent to setup function, sets up all pins numbers and pin modes
        """
        self.endswich1_pin = 13
        self.endswich2_pin = 11
        self.pumps_pin = [16, 18, 22, 24]
        self.motor_for_pin = 28
        self.motor_back_pin = 30
        self.selected_pump = 0
        self.glass_sensor = 15
        self.current_sensor = 26

        self.pouring_mode = 0
        self.pump_flowrate = 50
        self.glass_capacity = 200

        self.isWorking = False
        self.motor_mode = 0
        self.pwm = 100
        self.pwm_pin = 10


        self.pi = pigpio.pi()
        self.pouring_start_time = -1

        self.pi.set_mode(self.endswich1_pin, pigpio.INPUT)
        self.pi.set_mode(self.endswich2_pin, pigpio.INPUT)
        self.pi.set_mode(self.glass_sensor, pigpio.INPUT)
        self.pi.set_mode(self.current_sensor, pigpio.INPUT)
        self.pi.set_mode(self.motor_for_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.motor_back_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.pwm_pin, pigpio.OUTPUT)

        for i in self.pumps_pin:
            self.pi.set_mode(i, pigpio.OUTPUT)

    def start(self):
        """
        starts main loop
        """
        while True:
            self.loop()

    def loop(self):
        """
        Main loop

        Works according to _motor_mode and _puring_mode variables

        For _motor_mode equal:
        1: elevator goes up
        -1: elevator goes down
        0: evalator stays

        For _pouring_mode equal:
        1: pump works
        0: pump doesnt work
        """


        if self.motor_mode == 1:
            self.elevator_up()
            return
        elif self.motor_mode == -1:
            self.elevator_down()
            return

        elif self.pouring_mode == 1:
            if self.pouring_start_time < 0:
                self.pouring_start_time = self.get_current_time()

            self.pi.write(self.pumps_pin[self.selected_pump], pigpio.HIGH)

            if self.get_current_time() - self.pouring_start_time >= (self.glass_capacity/self.pump_flowrate*1000):
                self.set_motor_mode(1)
                self.pouring_mode = 0
                self.pouring_start_time = -1
                self.pi.write(self.pumps_pin[self.selected_pump], pigpio.LOW)

        elif self.pi.read(self.endswich1_pin) and self.motor_mode == 1:
            self.set_motor_mode(0)

        elif self.pi.read(self.endswich2_pin) and self.motor_mode == -1:
            self.set_motor_mode(0)
            self.pouring_mode = 1



    def elevator_down(self):
        """
        Turns elevator to go down
        """
        self.pi.write(self.motor_for_pin, pigpio.LOW)
        self.pi.write(self.motor_back_pin, pigpio.HIGH)
        self.pi.write(self.pwm_pin, self.pwm)

    def elevator_up(self):
        """
        Turns elevator to go up
        """
        self.pi.write(self.motor_for_pin, pigpio.HIGH)
        self.pi.write(self.motor_back_pin, pigpio.LOW)
        self.pi.write(self.pwm_pin, self.pwm)

    def elevator_stop(self):
        """
        Stops elevator
        """
        self.pi.write(self.motor_for_pin, pigpio.LOW)
        self.pi.write(self.motor_back_pin, pigpio.LOW)
        self.pi.write(self.pwm_pin, 0)


    async def elevator_begin(self):
        """
        Starts pouring sequent
        :return: 0 if pouring begins 1 if machine is occupied 2 if there is no glass found
        """

        if self.isWorking:
            return 1

        if not self.pi.read(self.current_sensor):
            return 2

        self.isWorking = True
        self.set_motor_mode(-1)

        return 0

    def select_pump(self, selected_pump):
        """
        Sets elevator mode to desired one (-1 for going down, 0 for staying and 1 for going up)
        :param selected_pump: sets pump to be used in pouring
        """
        self.selected_pump = selected_pump


    def set_motor_mode(self, mode):
        """
        Sets elevator mode to desired one (-1 for going down, 0 for staying and 1 for going up)
        :param mode: new mode of elevator
        """
        self.motor_mode = mode

    def get_current_time(self):
        """
        :return: current time in milliseconds
        """
        return int(round(time.time() * 1000))