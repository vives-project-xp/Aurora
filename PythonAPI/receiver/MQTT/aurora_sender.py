import requests
from paho.mqtt import client as mqtt_client
import random
import time

broker = 'broker.emqx.io'
port = 1883
wled = "wled/aurorawled"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'Aurora'
password = 'Aurora_420'


def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

client = mqtt_client.Client(client_id)
client.username_pw_set(username, password)
client.on_connect = on_connect
client.connect(broker, port)


class sender:
    connected = False
    def __init__(self):
        print("Sender started")
        self.run()
    
    def SetColor(self, data):
        red = data["red"]
        green = data["green"]
        blue = data["blue"]
        msg =  "#" + red + green + blue
        self.publish(wled + "/col", msg)


    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(client_id)
        client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(broker, port)
        return client


    def publish(self, topic, msg):
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {self.topic}")


    def run(self):
        client.loop_start()
        
