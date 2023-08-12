import time
import serial.tools.list_ports 

class RS485Controller:
    def __init__(self):
        self.ser = serial.Serial(port="/dev/ttyAMA2", baudrate=9600)
        
    def serial_read_data(self):
        bytesToRead = self.ser.inWaiting()
        if bytesToRead > 0:
            out = self.ser.read(bytesToRead)
            data_array = [b for b in out]
            # print(data_array)
            if len(data_array) >= 7:
                array_size = len(data_array)
                value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
                return value
            else:
                return -1
        return 0
    
    def relayController(self, number, state):
        relay_ON =  [[1, 6, 0, 0, 0, 255, 201, 138],
                     [2, 6, 0, 0, 0, 255, 201, 185],
                     [3, 6, 0, 0, 0, 255, 200, 104],
                     [4, 6, 0, 0, 0, 255, 201, 223],
                     [5, 6, 0, 0, 0, 255, 200, 14],
                     [6, 6, 0, 0, 0, 255, 200, 61],
                     [7, 6, 0, 0, 0, 255, 201, 236],
                     [8, 6, 0, 0, 0, 255, 201, 19]]
    
        relay_OFF = [[1, 6, 0, 0, 0, 0, 137, 202],
                     [2, 6, 0, 0, 0, 0, 137, 249],
                     [3, 6, 0, 0, 0, 0, 136, 40],
                     [4, 6, 0, 0, 0, 0, 137, 159],
                     [5, 6, 0, 0, 0, 0, 136, 78],
                     [6, 6, 0, 0, 0, 0, 136, 125],
                     [7, 6, 0, 0, 0, 0, 137, 172],
                     [8, 6, 0, 0, 0, 0, 137, 83]]
        
        if state == 0:
            self.ser.write(relay_OFF[number - 1])
            print(self.serial_read_data())
        else:
            self.ser.write(relay_ON[number - 1])
            print(self.serial_read_data())
    
    def getvalueDistance(self, number):
        distance_9 = [9, 3, 0, 5, 0, 1, 149, 67]
        distance_12 = [12, 3, 0, 5, 0, 1, 149, 22]
        
        if number == 9:
            self.ser.write(distance_9)
            time.sleep(0.3)
            distance = self.serial_read_data()
            print("Distance of sensor 09: ",distance)
        elif number == 12:
            self.ser.write(distance_12)
            time.sleep(0.3)
            distance = self.serial_read_data()
            print("Distance of sensor 12: ",distance)
        else:
            print("The input gate is entered incorrectly")
        return distance
        