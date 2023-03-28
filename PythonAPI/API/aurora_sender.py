import requests
from paho.mqtt import client as mqtt_client
import random
import time
import json
from threading import Thread, Timer

broker = 'broker.emqx.io'
port = 1883
wled = "wled/aurorawled"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'Aurora'
password = 'Aurora_420'

minDistance = 50
delay = 1
threads = []

def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Aurora sender: Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

client = mqtt_client.Client(client_id)
client.username_pw_set(username, password)
client.on_connect = on_connect
client.connect(broker, port)


class sender:
    connected = False
    def __init__(self):
        print("API Sender started")
        self.run()

    def Toggle(self):
         print("toggle")
         self.publish(wled, "T")


    def SetColor(self, data):
        red = data["red"]
        green = data["green"]
        blue = data["blue"]
        msg =  '{"seg":[{"col":[['+ red + ','+green +',' + blue + ']]}]}'
        self.publish(wled + "/api", msg)

    def SetPreset(self, data):
        print("setpreset")
        ps = data["ps"]
        msg = '{"ps":' +ps +'}'
        self.publish(wled + "/api", msg)

    def publish(self, topic, msg):
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
            return
        else:
            print(f"Failed to send message to topic {self.topic}")

    def Sensor(self, data):
         sensor = data["sensor"]
         distance = data["distance"]
         print(sensor, distance)
         if(distance >= minDistance or distance < 0): return
         else:
              #print(sensor)
              self.CreateSegment(sensor + 1)
    
    def CreateSegment(self, id):
         msg = '{"seg":[{"id":' + str(id) + ',"frz":false}]}'
         self.publish(wled + "/api", msg)
         threads.append(id)
         t = Timer(delay, self.Task, args=[id])
         t.start()

    def Task(self, id):
        threads.remove(id)
        if(id in threads): 
                return
        else:
            msg = '{"seg":[{"id":' + str(id) + ',"frz":true}]}'
            self.publish(wled + "/api", msg)
            return
                
    def run(self):
        client.loop_start()
