from flask import Flask, json, request, render_template, make_response
from flask_mqtt import Mqtt
from flask_cors import CORS
import requests
from aurora_sender import sender
import datetime

sender = sender()
app = Flask(__name__)
CORS(app)
app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
app.config['MQTT_USERNAME'] = 'Aurora'  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = 'Aurora_420'  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

mqtt = Mqtt(app)

@app.route('/', methods=['GET'])
def main():
    print("connecting...")
    return render_template('index.html')

@app.route('/color', methods=['POST'])
def color():
    print("receive", datetime.datetime.today())
    json = request.get_json()
    sender.SetColor(json)
    return ('', 204)

@app.route('/connect', methods=['POST'])
def connect():
    connect = sender.Connect(request.get_json())
    response = make_response()
    response.headers['info'] = connect
    return response

def create_app():
    app = Flask(__name__)
    mqtt.init_app(app)
    
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Connected to Broker")
    mqtt.subscribe('aurora_sensor')

@mqtt.on_subscribe()
def handle_subscribe(client, userdata, mid, granted_qos):
    print('Subscription id {} granted with qos {}.'
          .format(mid, granted_qos)) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)