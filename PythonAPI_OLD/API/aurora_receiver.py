from flask import Flask, json, request, render_template, make_response, redirect, jsonify
from flask_mqtt import Mqtt
from flask_cors import CORS
from aurora_sender import sender
from threading import Timer


sender = sender()

app = Flask(__name__)
CORS(app)
app.config['MQTT_BROKER_URL'] = 'mosquitto' #broker url
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
#app.config['MQTT_USERNAME'] = 'Aurora'  # set the username here if you need authentication for the broker
#app.config['MQTT_PASSWORD'] = 'Aurora_420'  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes
app.config['MQTT_CLIENT_ID'] = "Aurora_receiver"
topic_sensor = "aurora/sensor"
topic_connect = "aurora/sensor/connect"

mqtt = Mqtt(app)

@app.route('/', methods=['GET'])
def main():
    return redirect("website", code=302)

@app.route('/color', methods=['POST'])
def color():
    json = request.get_json()
    sender.SetColor(json)
    return ("", 204)

@app.route('/preset', methods=['POST'])
def preset():
    json = request.get_json()
    sender.SetPreset(json)
    return ("", 204)

@app.route('/toggle', methods=['POST'])
def toggle():
    sender.Toggle()
    return ("", 204)

@app.route('/sensors', methods=['POST'])
def sensors():
        data = sender.Sensors()
        response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
        )
        return response

@app.route('/updatesensor', methods=['POST'])
def updatesensor():
    json = request.get_json()
    sender.UpdateSensor(json)
    return ("", 204)


def create_app():
    app = Flask(__name__)
    connect()

def connect():
     try:
        mqtt.init_app(app)
     except:
         return
    
connected = False

def UpdateConnect(connected_old):
    global connected
    connected = not connected_old

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("API receiver: Connected to Broker")
    UpdateConnect(connected)
    mqtt.subscribe(topic_sensor)
    mqtt.subscribe(topic_connect)

@mqtt.on_subscribe()
def handle_subscribe(client, userdata, mid, granted_qos):
    print('Subscription id {} granted with qos {}.'
          .format(mid, granted_qos))
    
@mqtt.on_message()
def handle_message(client, userdata, msg):
    #print(msg.topic,str(msg.payload.decode()))
    if msg.topic == topic_connect:
        msg = json.loads(str(msg.payload.decode()))
        sender.ConnectSensor(msg)
        sensor = str(str(msg["id"]).removeprefix("Aurora_sensor"))
        mqtt.subscribe(topic_sensor + "/" + sensor + "/dist")
    elif topic_sensor in msg.topic:
        sender.Sensor(json.loads(str(msg.payload.decode())))

@mqtt.on_disconnect()
def handle_disconnect():
    print("Aurora_Receiver DISCONNECTED")
    UpdateConnect(connected)
    connect()

def reconnect():
        Timer(10, reconnect).start()
        if not connected:
            print("Aurora_receiver: reconnecting...")
            connect()
            return


reconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)
