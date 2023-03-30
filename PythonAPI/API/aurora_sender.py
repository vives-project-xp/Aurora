import requests
from paho.mqtt import client as mqtt_client
import random
import time
import json
from threading import Thread, Timer
from configparser import ConfigParser

broker = 'mqtt.devbit.be'
port = 1883
topic_wled = "aurora/wled"
topic_sensor = "aurora/sensor"
# generate client ID with pub prefix randomly
client_id = f'Aurora_Sender'
username = 'Aurora'
password = 'Aurora_420'
sensordata = "/data/sensordata.ini"
connected = False
config_object = ConfigParser()
minDistance = 20
delay = 1
threads = []

class sender:
    connected = False
    def on_connect(self, client, userdata, flags, rc):
        if self.connected == False:
            if rc == 0:
                print("Aurora sender: Connected to MQTT Broker!")
                self.connected = True
            else:
                print("Failed to connect, return code %d\n", rc)

    def __init__(self):
        print("API Sender started")
        global client
        client = mqtt_client.Client(client_id)
        client.username_pw_set(username, password)
        client.on_connect = self.on_connect
        client.connect(broker, port)
        self.run(client)
        

    def Toggle(self):
         print("toggle")
         self.publish(topic_wled, "T")


    def SetColor(self, data):
        #print(json.dumps(data))
        red = data["red"]
        green = data["green"]
        blue = data["blue"]
        msg =  '{"seg":[{"col":[['+ red + ','+green +',' + blue + ']]}]}'
        self.publish(topic_wled + "/api", msg)

    def SetPreset(self, data):
        print("setpreset")
        ps = data["ps"]
        msg = '{"ps":' +ps +'}'
        self.publish(topic_wled + "/api", msg)

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
         #print(sensor, distance)
         if(distance >= minDistance or distance < 0): return
         else:
              #print(sensor)
              self.CreateSegment(sensor + 1)
    
    def CreateSegment(self, id):
         msg = '{"seg":[{"id":' + str(id) + ',"frz":false}]}'
         self.publish(topic_wled + "/api", msg)
         threads.append(id)
         t = Timer(delay, self.Task, args=[id])
         t.start()

    def Task(self, id):
        threads.remove(id)
        if(id in threads): 
                return
        else:
            msg = '{"seg":[{"id":' + str(id) + ',"frz":true}]}'
            self.publish(topic_wled + "/api", msg)
            return
        
    def ConnectSensor(self, msg):
         config_object.read(sensordata)
         sensor = str(msg["id"]).removeprefix("Aurora_sensor")
         try:
             count = config_object["sensorCount"]
         except:
             config_object["sensorCount"] = {"count": 0}
             self.SaveConfig()
         try:
            data = config_object[sensor]
            self.publish(topic_sensor + "/connected", "you are connected")
         except:
            count = int(config_object["sensorCount"]["count"])
            config_object[sensor] = {"id": count}
            config_object["sensorCount"] = {"count": count + 1}
            print("added new sensor:", sensor, "with id:" , count)
            self.publish(topic_sensor + "/connect", "you are connected")
            self.SaveConfig()
            return

    def SaveConfig(self):
         with open(sensordata, 'w') as conf:
             config_object.write(conf)
                
    def run(self, client):
        client.loop_start()
