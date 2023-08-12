import enum

from softwaretimer import *
from RS485Controller import *

class Status(enum.Enum):
    INIT = 1
    PUMP_ON1 = 2
    PUMP_OFF1 = 3
    PUMP_ON2 = 4
    PUMP_OFF2 = 5
    PUMP_ON3 = 6
    PUMP_OFF3 = 7
    STABLE = 8
    IDLE = 9
    RELAY_IN = 12
    RELAY_OUT = 13
    SENSOR1 = 10
    SENSOR2 = 11

class Monitoring:
    PUMP_ON_DELAY = [3000, 4000, 5000, 0, 1000, 0]
    PUMP_OFF_DELAY = [5000, 5000, 5000]
    STABLE_DELAY = 5000
    SENSING_DELAY = 500
    IDLE_DELAY = 10000
    BUTTON_STATE = []
    numButton = 8
    count = 0
    distance1_value = 1
    distance2_value = 2

    def __init__(self, soft_timer, rs485):
        self.soft_timer = soft_timer
        self.rs485 = rs485
        self.status = Status.INIT
        self.BUTTON_STATE = [False] * self.numButton

    def relayController(self, number, state):
        self.rs485.relayController(number, state)

    def distanceController(self, number):
        self.rs485.distanceController(number)

    def getDistance(self):
        self.distanceStatus = Status.INIT

    def MonitoringTask_Run(self):
        def switch_case(status):
            switcher = {
                Status.INIT: self.handle_init,
                Status.PUMP_ON1: self.handle_pump_on1,
                Status.PUMP_OFF1: self.handle_pump_off1,
                Status.PUMP_ON2: self.handle_pump_on2,
                Status.PUMP_OFF2: self.handle_pump_off2,
                Status.PUMP_ON3: self.handle_pump_on3,
                Status.PUMP_OFF3: self.handle_pump_off3,
                Status.STABLE: self.handle_stable,
                Status.IDLE: self.handle_idle,
                Status.RELAY_IN: self.handle_relay_in,
                Status.RELAY_OUT: self.handle_relay_out,
                Status.SENSOR1: self.handle_sensor1,
                Status.SENSOR2: self.handle_sensor2,
            }
            return switcher.get(status, self.handle_invalid_status)()

        switch_case(self.status)

    def handle_init(self):
        print("Init")
        if self.PUMP_ON_DELAY[0] == 0:
            self.status = Status.PUMP_ON2
        else:
            self.soft_timer.set_timer(0, self.PUMP_ON_DELAY[0])
            self.status = Status.PUMP_ON1
            self.BUTTON_STATE[0] = True

    def handle_pump_on1(self):
        if self.soft_timer.is_timer_expired(0):
            print("pump_on1")
            self.soft_timer.set_timer(0, self.PUMP_OFF_DELAY[0])
            self.status = Status.PUMP_OFF1
            self.BUTTON_STATE[0] = False

    def handle_pump_off1(self):
        if self.soft_timer.is_timer_expired(0):
            print("pump_off1")
            if self.PUMP_ON_DELAY[1] == 0:
                self.status = Status.PUMP_ON3
            else:
                self.soft_timer.set_timer(0, self.PUMP_ON_DELAY[1])
                self.status = Status.PUMP_ON2
                self.BUTTON_STATE[1] = True

    def handle_pump_on2(self):
        if self.soft_timer.is_timer_expired(0):
            print("pump_on2")
            self.soft_timer.set_timer(0, self.PUMP_OFF_DELAY[1])
            self.status = Status.PUMP_OFF2
            self.BUTTON_STATE[1] = False

    def handle_pump_off2(self):
        if self.soft_timer.is_timer_expired(0):
            print("pump_off2")
            if self.PUMP_ON_DELAY[2] == 0:
                self.status = Status.STABLE
                self.soft_timer.set_timer(0, self.STABLE_DELAY)
            else:
                self.soft_timer.set_timer(0, self.PUMP_ON_DELAY[2])
                self.status = Status.PUMP_ON3
                self.BUTTON_STATE[2] = True

    def handle_pump_on3(self):
        if self.soft_timer.is_timer_expired(0):
            print("pump_on3")
            self.soft_timer.set_timer(0, self.PUMP_OFF_DELAY[2])
            self.status = Status.PUMP_OFF3
            self.BUTTON_STATE[2] = False

    def handle_pump_off3(self):
        if self.soft_timer.is_timer_expired(0):
            print("pump_off3")
            self.status = Status.STABLE
            self.soft_timer.set_timer(0, self.STABLE_DELAY)

    def handle_stable(self):
        if self.soft_timer.is_timer_expired(0):
            print("End")

    def handle_idle(self):
        pass

    def handle_relay_in(self):
        pass

    def handle_relay_out(self):
        pass

    def handle_sensor1(self):
        pass

    def handle_sensor2(self):
        pass

    def handle_invalid_status(self):
        print("Invalid status")
