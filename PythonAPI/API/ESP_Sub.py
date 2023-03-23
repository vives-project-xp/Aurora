import random
#..MQTTPython.
from paho.mqtt import client as mqtt_client

print("ESP receiver started")
broker = 'broker.emqx.io'
port = 1883
#topic = "aurora/sensor_1/hello"
topic_0 = "aurora/sensor_0/measurements"
topic_1 = "aurora/sensor_1/measurements"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'Aurora'
password = 'Aurora_420'

class sub:
    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("ESP receiver: Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(client_id)
        client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(broker, port)
        return client


    def subscribe(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        client.subscribe(topic_0)
        client.subscribe(topic_1)
        client.on_message = on_message


    def run(self):
        client = self.connect_mqtt()
        self.subscribe(client)
        client.loop_forever()
