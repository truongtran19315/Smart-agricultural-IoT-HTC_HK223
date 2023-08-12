import time
from Adafruit_IO import MQTTClient
print("Sensors and Actuators")
import serial.tools.list_ports


def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        print(strPort) # print(strPort)
        if "/dev/ttyAMA2" in strPort:
            splitPort = strPort.split(" ")
            print("PortName:",strPort)
            commPort = splitPort[0]
    return commPort


portName = getPort()
print("portName:",portName)
if portName != "None":
    ser = serial.Serial(port=portName, baudrate=9600)

relay1_ON = [0, 6, 0, 0, 0, 255, 200, 91]
relay1_OFF = [0, 6, 0, 0, 0, 0, 136, 27]


def setDevice1(state):
    serial_read_data(ser)
    #print(ser)
    if state == True:
        ser.write(relay1_ON)
        client.publish(AIO_FEED_ID[2],1)
    else:
        ser.write(relay1_OFF)
        client.publish(AIO_FEED_ID[2],0)


relay2_ON = [15, 6, 0, 0, 0, 255, 200, 164]
relay2_OFF = [15, 6, 0, 0, 0, 0, 136, 228]


def setDevice2(state):
    serial_read_data(ser)
    #print(ser)
    if state == True:
        ser.write(relay2_ON)
        #client.publish(AIO_FEED_ID[3],1)
    else:
        ser.write(relay2_OFF)
        #client.publish(AIO_FEED_ID[3],0)


def serial_read_data(ser):
    bytesToRead = ser.inWaiting()
    if bytesToRead > 0:
        out = ser.read(bytesToRead)
        data_array = [b for b in out]
        print(data_array)
        if len(data_array) >= 7:
            array_size = len(data_array)
            value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
            return value
        else:
            return -1
    return 0


soil_temperature = [3,
          3,
          0,
          0,
          0,
          1,
          133,
          232
]


def readTemperature():
    serial_read_data(ser)# doc dang co trong buff cà xoa het buffer.
    ser.write(soil_temperature)
    time.sleep(1)
    temp = serial_read_data(ser)
    client.publish(AIO_FEED_ID[1],temp)
    return temp


soil_moisture = [3,
          3,
          0,
          1,
          0,
          1,
          212,
          40]


def readMoisture():
    serial_read_data(ser)
    ser.write(soil_moisture)
    time.sleep(1)
    client.publish(AIO_FEED_ID[0],serial_read_data(ser))
    return serial_read_data(ser)

##Adafruit
AIO_FEED_ID = ["ttnt-humi", "ttnt-temp", "ttnt-relay1"]
AIO_USERNAME = "haingoquang"
AIO_KEY = "aio_uZjH00KzIDHZ6SLXIhg8uWZwtfDK"



# THUC HIEN HANH CHUC NANG


def connected(client):
    print("E ket noi thanh cong Adafruit roi do ...")
    client.subscribe(AIO_FEED_ID)

def subscribe(client, userdata , mid , granted_qos):
    print("Sub Successful ...")


def disconnected(client):
    print("DISCONECT ...")
    sys.exit(1)


def message(client, feed_id, payload):
    # if feed_id == AIO_FEED_ID[2]:
    #     print("Turn relay 1:" + payload)
    #     #ser.write((payload+'#').encode('UTF-8'))
    print("Data come")
    print("Turn relay 1:" + payload)
    if feed_id == AIO_FEED_ID[3]:
        print("Data Temp :" + payload)
        #ser.write((str(payload) + "#").encode())


client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_message = message
client.on_disconnect = disconnected
client.on_subscribe = subscribe
client.connect()
client.loop_background()

while True:
    # print("TEST MOTOR")
    # setDevice1(True)
    # time.sleep(2)
    # setDevice1(False)
    # time.sleep(2)
    
    # setDevice2(True)
    # time.sleep(2)
    # setDevice2(False)
    # time.sleep(2)
    setDevice1(True)
    #print(readMoisture())
   # print(ser.read())
    time.sleep(2)

