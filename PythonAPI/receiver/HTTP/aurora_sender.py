import requests

class sender:
    wled = "http://aurorawled.local/"
    connected = False
    def __init__(self):
        print("Sender started")
        print(self.wled)
    
    def Connect(self, data):
        print("connecting")
        self.wled = "http://" + data["wled"] + "/"
        print(self.wled)
        try:
            requests.post(self.wled)
            print(requests)
            self.connected = True
            print("connected to wled")
            return "connected"
        except:
            self.connected = False
            print('wrong url')
            return "wrong_url"
    
    def SetColor(self, data):
        if(self.connected):
            red = "&R=" + data["red"]
            green = "&G=" + data["green"]
            blue = "&B=" + data["blue"]
            url =  self.wled + 'win' + red + green + blue
            requests.post(url)