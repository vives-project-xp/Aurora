from flask import Flask, json, request, render_template
import requests
api = Flask(__name__)
import aurora
#aurora = Aurora.getClass()
class FlaskAPI:
    def __init__(self):
        print("flaskapi loaded")

    def start():
        print("server starting")
        #if __name__ == '__main__':
        api.run(host='0.0.0.0')


    @api.route('/', methods=['GET', 'POST'])
    def main():
        return render_template('index.html')

    @api.route('/color', methods=['POST', 'GET'])
    def color():
        json = request.get_json()
        aurora.Aurora.setColor(json)
        return render_template('index.html')
        
    #if __name__ == '__main__':
    api.run(host='0.0.0.0')