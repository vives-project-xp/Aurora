import Flask.flaskapi as flaskapi
import requests

class Aurora():
    def __init__(self) -> None:
        pass

    def getClass():
        return Aurora
    def setColor(color):
        red = "&R=" + color["red"]
        green = "&G=" + color["green"]
        blue = "&B=" + color["blue"]
        url = 'http://auroraWLED.local/win' + red + green + blue
        requests.post(url)
        return print(color)

