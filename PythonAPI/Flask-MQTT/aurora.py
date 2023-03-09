import Flask.flaskapi as flaskapi
import MQTT.MQTTPython.MQTT_test_Sub as mqtt
import requests
site = 'http://auroraWLED.local/win'
class Aurora():
    def __init__(self) -> None:
        pass

    def getClass():
        return Aurora
    def setColor(color):
        red = "&R=" + color["red"]
        green = "&G=" + color["green"]
        blue = "&B=" + color["blue"]
        url = site + red + green + blue
        requests.post(url)
        return print(color)

