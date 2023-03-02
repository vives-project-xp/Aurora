from flask import Flask, json, request, render_template
import requests

api = Flask(__name__)

@api.route('/', methods=['GET'])
def main():
    return render_template('index.html')

@api.route('/color', methods=['POST', 'GET'])
def color():
    json = request.get_json()
    print(json)
    red = "&R=" + json["red"]
    green = "&G=" + json["green"]
    blue = "&B=" + json["blue"]
    url = 'http://aurora.local/win' + red + green + blue
    response = requests.post(url)
    return print(type(json))

if __name__ == '__main__':
    api.run(debug = True)
