import requests
from paho.mqtt import client as mqtt_client
import random
from datetime import datetime
import json
from threading import Thread, Timer
from configparser import ConfigParser
import pytz

broker = 'mosquitto'
port = 1883
topic_wled = "aurora/wled"
topic_sensor = "aurora/sensor"
# generate client ID with pub prefix randomly
client_id = f'Aurora_Sender'
username = 'Aurora'
password = 'Aurora_420'
sensordata = "/data/sensordata.ini"
connected = False
config = ConfigParser()
maxDistance = 100
minDistance = 0
delay = 1
measurements = []
threads = []
timezone = pytz.timezone('Europe/Brussels')

class sender:
    connected = False
    sensorId = 0
    def on_connect(self, client, userdata, flags, rc):
        if self.connected == False:
            if rc == 0:
                print("Aurora sender: Connected to MQTT Broker!")
                self.connected = True
                self.MeasureTask()
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

    def Sensors(self):
         config.read(sensordata)
         if not config.has_section("data"): return
         if not config.has_section("sensors"): return
         msg = []
         msg.clear
         for (sensor, data) in list(config.items("sensors")):
            data = json.loads(config.get("sensors", sensor))
            msg.append(data)
         return msg
    
    def UpdateSensor(self, data):
        sensor = data["name"]
        id = data["id"]
        data = json.loads(config.get("sensors", sensor))
        data["id"] = str(id)
        config.set("sensors", str(sensor), str(data).replace("'", '"'))
        self.SaveConfig()


    def SetColor(self, data):
        #print(json.dumps(data))
        red = data["red"]
        green = data["green"]
        blue = data["blue"]
        msg =  '{"seg":[{"col":[['+ red + ','+green +',' + blue + ']]}]}'
        self.publish(topic_wled + "/api", msg)

    def SetPreset(self, data):
        ps = data["ps"]
        msg = '{"ps":' +str(ps) +'}'
        self.publish(topic_wled + "/api", msg)

    def publish(self, topic, msg):
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            #print(f"Send `{msg}` to topic `{topic}`")
            return
        else:
            print(f"Failed to send `{msg}` to topic {topic}", status)

    def Sensor(self, data):
         config.read(sensordata)
         id = str(data["id"]).removeprefix("Aurora_sensor")
         distance = data["distance"]
         data = json.loads(config.get("sensors", id))
         data["lastseen"] = str(datetime.now(tz=timezone).strftime("%d/%m/%Y %H:%M:%S"))
         config.set("sensors", str(id), str(data).replace("'", '"'))
         self.SaveConfig()
         #print(id, distance)
         if(distance >= maxDistance or distance < minDistance):
            if(id in measurements):
                measurements.remove(id)
                print("removed", id)
         else:
            if(id in measurements):
              #print(sensor)
              self.CreateSegment(int(json.loads(config.get("sensors", id))["id"]) + 1)
            else:
                print("added", id)
                measurements.append(id)
    
    def CreateSegment(self, id):
         if id not in threads:
            print(id, "on")
            msg = '{"seg":[{"id":' + str(id) + ',"frz":false}]}'
            self.publish(topic_wled + "/api", msg)
         threads.append(id)
         t = Timer(delay, self.ColorTask, args=[id])
         t.start()

    def ColorTask(self, id):
        threads.remove(id)
        if(id in threads): 
                return
        else:
            print(id, "off")
            msg = '{"seg":[{"id":' + str(id) + ',"frz":true}]}'
            self.publish(topic_wled + "/api", msg)
    
    def MeasureTask(self):
        config.read(sensordata)
        if config.has_section("sensors"):
            if(self.sensorId == 0):
                for (sensor,data) in list(config.items("sensors")):
                    try:
                        data = json.loads(config.get("sensors", sensor))
                    except:
                        return
                    if (int(data["id"])+1) % 2 == 0:
                            self.Measure(sensor)
                self.sensorId = 1
            else:
                for (sensor,data) in list(config.items("sensors")):
                    data = json.loads(config.get("sensors", sensor))
                    if (int(data["id"])+1) % 2 != 0:
                            self.Measure(sensor)
                self.sensorId = 0
        Timer(0.06,self.MeasureTask).start()

    def Measure(self, sensor):
               msg = '{"cmd":"measure","sensor":"' + str(sensor) +'"}'
               self.publish(topic_sensor + "/" + sensor + "/measure", msg)    
        
    def ConnectSensor(self, msg):
         config.read(sensordata)
         sensor = str(str(msg["id"]).removeprefix("Aurora_sensor"))
         #Check if data exists
         if not config.has_section("data"):
              config.add_section("data")
              config.set("data", "sensorcount", "0")
        #Check if sensors exists
         if not config.has_section("sensors"):
            config.add_section('sensors')

         if not config.has_option("sensors" , sensor):
            count = int(config.get("data","sensorcount"))
            data = '{"name":"'+sensor + '","id":"' + str(count)+ '","lastseen":"' + str(datetime.now(tz=timezone).strftime("%d/%m/%Y %H:%M:%S")) + '"}'
            config.set("sensors", sensor, data)
            config.set("data", "sensorcount", str(count + 1))
            print("added new sensor:", sensor, "with id:" , count)
         self.SaveConfig()
         self.publish(topic_sensor + "/" + sensor +"/connected", '{"cmd":"connected","sensor":"' + str(sensor) +'"}')

    def SaveConfig(self):
         with open(sensordata, 'w') as conf:
             config.write(conf)
                
    def run(self, client):
        client.loop_start()
