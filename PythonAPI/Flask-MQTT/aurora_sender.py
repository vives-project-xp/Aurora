import requests

class sender:
    wled = ""
    connected = False
    def __init__(self):
        print("Sender started")
    
    def Connect(self, data):
        self.wled = "http://" + data["wled"] + "/"
        print(self.wled)
        try:
            requests.post(self.wled)
            self.connected = True
            return "connected"
        except:
            self.connected = False
            return "wrong_url"
    
    def SetColor(self, data):
        if(self.connected):
            red = "&R=" + data["red"]
            green = "&G=" + data["green"]
            blue = "&B=" + data["blue"]
            url =  self.wled + 'win' + red + green + blue
            requests.post(url)