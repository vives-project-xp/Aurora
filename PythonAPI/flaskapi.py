from flask import Flask, json, request, render_template
import requests

api = Flask(__name__)

@api.route('/', methods=['GET','POST'])
def color():
    args = request.args
    red = "&R=" + str(args.get("r"))
    green = "&G=" + str(args.get("g"))
    blue = "&B=" + str(args.get("b"))
    url = 'http://aurora.local/win' + red + green + blue
    response = requests.post(url)
    return render_template('index.html')

if __name__ == '__main__':
    api.run(debug = True)
