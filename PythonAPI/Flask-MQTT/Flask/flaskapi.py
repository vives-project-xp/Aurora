from flask import Flask, json, request, render_template
import requests
import aurora
api = Flask(__name__)
class FlaskAPI:
    def __init__(self):
        print("flaskapi loaded")

    def start():
        print("server starting")
        api.run(host='0.0.0.0')


    @api.route('/', methods=['GET', 'POST'])
    def main():
        return render_template('index.html')

    @api.route('/color', methods=['POST', 'GET'])
    def color():
        json = request.get_json()
        aurora.Aurora.setColor(json)
        return render_template('index.html')
        
    api.run(host='0.0.0.0')