from flask import Flask, json, request, render_template
import requests
import datetime

api = Flask(__name__)

@api.route('/', methods=['GET'])
def main():
    return render_template('index.html')

@api.route('/color', methods=['POST', 'GET'])
def test():
    json = request.get_json()
    red = "&R=" + json["red"]
    green = "&G=" + json["green"]
    blue = "&B=" + json["blue"]
    url = 'http://auroraWLED.local/win' + red + green + blue
    requests.post(url)
    return render_template('index.html')

if __name__ == '__main__':
    api.run(host='0.0.0.0')
