# python 3.6

import random
import time
import json

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883  
topic_0 = "aurora/sensor_0/esp32-sonic-f10f7c/commands"
topic_1 = "aurora/sensor_1/esp32-sonic-e37fa4/commands"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'Aurora'
password = 'Aurora_420'

def connect_mqtt():
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


def publish(client):
    msg_count = 0
    while True:
        time.sleep(0.25)
        msg = json.dumps({"cmd":"measure" })
        result_0 = client.publish(topic_0, msg)
        status_0 = result_0[0]
        if status_0 == 0:
            print(f"Send `{msg}` to topic `{topic_0}`")
        else:
            print(f"Failed to send message to topic {topic_0}")
        time.sleep(0.25)
        result_1 = client.publish(topic_1, msg)
        # result: [0, 1]
        status_1 = result_0[0]
        if status_1 == 0:
            print(f"Send `{msg}` to topic `{topic_1}`")
        else:
            print(f"Failed to send message to topic {topic_1}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
