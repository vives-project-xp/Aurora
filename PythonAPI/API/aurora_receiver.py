from flask import Flask, json, request, render_template, make_response, redirect
from flask_mqtt import Mqtt
from flask_cors import CORS
from aurora_sender import sender


sender = sender()

app = Flask(__name__)
CORS(app)
app.config['MQTT_BROKER_URL'] = 'Mosquitto' #broker url
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
#app.config['MQTT_USERNAME'] = 'Aurora'  # set the username here if you need authentication for the broker
#app.config['MQTT_PASSWORD'] = 'Aurora_420'  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes
app.config['MQTT_CLIENT_ID'] = "Aurora_receiver"
topic = "aurora_sensor"

mqtt = Mqtt(app)

@app.route('/', methods=['GET'])
def main():
    mqtt.init_app(app)
    return redirect("http://aurora.local", code=302)

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


def create_app():
    app = Flask(__name__)
    mqtt.init_app(app)
    
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("API receiver: Connected to Broker")
    mqtt.subscribe(topic)

@mqtt.on_subscribe()
def handle_subscribe(client, userdata, mid, granted_qos):
    print('Subscription id {} granted with qos {}.'
          .format(mid, granted_qos))
    
@mqtt.on_message()
def handle_message(client, userdata, msg):
    print(str(msg.payload.decode()))
    sender.Sensor(json.loads(str(msg.payload.decode())))

@mqtt.on_disconnect()
def handle_disconnect():
    print("Aurora_Receiver DISCONNECTED")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)