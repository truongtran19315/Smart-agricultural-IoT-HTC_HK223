import enum

class WMR_Status(enum.Enum):
    INIT = 1
    PUMP_ON = 2
    PUMP_OFF = 3
    STABLE = 6
    READSENSOR1 = 4
    READSENSOR2 = 5
    IDLE = 7
    
class MonitoringTask:
    PUMP_ON_DELAY = 3000
    PUMP_OFF_DELAY = 5000
    STABLE_DELAY = 20000
    SENSING_DELAY = 500
    IDLE_DELAY = 10000
    SENSOR1_Value=0
    SENSOR1_Value=0
    BUTTON_STATE = [False, False, False, False, False, False, False, False]

    def __init__(self, _rs485, _soft_timer):
        self.status = WMR_Status.INIT
        self.rs485=_rs485
        self.soft_timer = _soft_timer
        #self.client=Adafruit(AIO_USERNAME, AIO_KEY, AIO_FEED_ID)
        #self.client.connect() 
        
    def relayController(self, number, state):
        self.rs485.relayController(number,state)
    
    def getvalueDistance(self, number):
        dist=self.rs485.getvalueDistance(number)
        print("Khoang cach la: ",dist)
        return dist
        #self.client.mqtt_client.publish(AIO_FEED_ID[2],distance)

    def MonitoringTask_Run(self):

        if self.status == WMR_Status.INIT:
            self.soft_timer.set_timer(0, self.PUMP_ON_DELAY)
            self.status = WMR_Status.PUMP_ON
            print("PUMP is ON")
            self.BUTTON_STATE[6] = True
            self.relayController(7,1)
        
        elif self.status == WMR_Status.PUMP_ON:
            if self.soft_timer.is_timer_expired(0) == 1:
                self.status = WMR_Status.PUMP_OFF
                self.soft_timer.set_timer(0, self.PUMP_OFF_DELAY)
                print("PUMP is OFF...")
                self.BUTTON_STATE[6] = False
                self.relayController(7,0)

        elif self.status == WMR_Status.PUMP_OFF:
            if self.soft_timer.is_timer_expired(0) == 1:
                self.status = WMR_Status.STABLE
                self.soft_timer.set_timer(0, self.STABLE_DELAY)
                print("STABLIZING...")

        elif self.status == WMR_Status.STABLE:
            if self.soft_timer.is_timer_expired(0) == 1:
                self.SENSOR1_Value=self.getvalueDistance(9)
                print("Reading Distance Sensor 1 Value: ", self.SENSOR1_Value)
                self.status = WMR_Status.READSENSOR1
                self.soft_timer.set_timer(0, self.SENSING_DELAY)

        elif self.status == WMR_Status.READSENSOR1:
            if self.soft_timer.is_timer_expired(0) == 1:
                self.SENSOR2_Value=self.getvalueDistance(12)
                print("Reading Distance Sensor 2 Value: ", self.SENSOR2_Value)
                self.status = WMR_Status.READSENSOR2
                self.soft_timer.set_timer(0, self.SENSING_DELAY)

        elif self.status == WMR_Status.READSENSOR2:
            if self.soft_timer.is_timer_expired(0) == 1:
                self.status = WMR_Status.INIT
                print("INIT")

        else:
            print("Invalid status!!!")
        return

        
        

    







