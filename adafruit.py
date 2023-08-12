from Adafruit_IO import MQTTClient
import  sys
import time

class Adafruit:
    def __init__(self, username, key, feed_id_list):
        self.username = username
        self.feed_id_list = feed_id_list
        self.key = key
        self.mqtt_client = None

    def connected(self, client):
        print("Ket noi thanh cong Adafruit..")
        for feed_id in self.feed_id_list:
            print("Subscribe to " + feed_id)
            client.subscribe(feed_id)

    def subscribe(self, client, userdata , mid , granted_qos):
        print("Sub Successful ...")

    def disconnected(client):
        print("DISCONECT ...")
        sys.exit(1)

    def message(self, client, feed_id, payload):
        print("Data come")
        print("Turn relay 1:" + payload)
        if feed_id == self.feed_id_list[2]:
            print("Data Temp :" + payload)
            #ser.write((str(payload) + "#").encode())

    def connect(self):
        self.mqtt_client= MQTTClient(self.username,self.key)
        self.mqtt_client.on_connect=self.connected
        self.mqtt_client.on_disconnect = self.disconnected
        self.mqtt_client.on_message = self.message
        self.mqtt_client.on_subscribe = self.subscribe
        self.mqtt_client.connect()
        self.mqtt_client.loop_background()

AIO_FEED_ID = ["ttnt-humi", "ttnt-temp", "ttnt-relay1"]
AIO_USERNAME = "haingoquang"
AIO_KEY = "aio_JhIE9228jpE80KKYNAgeyHZVOG7y"

# while(True) :
#     client=Adafruit(AIO_USERNAME, AIO_KEY, AIO_FEED_ID)
#     client.connect()
#     time.sleep(2) 

# client=Adafruit(AIO_USERNAME, AIO_KEY, AIO_FEED_ID)
# client.connect()          
