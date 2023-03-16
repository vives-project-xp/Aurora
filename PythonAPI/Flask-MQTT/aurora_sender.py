import requests

class sender:
    wled = "aurorawled.local"
    connected = False
    def __init__(self):
        print("Sender started")
    
    def Connect(self, data):
        self.wled = "http://" + data["wled"] + "/"
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