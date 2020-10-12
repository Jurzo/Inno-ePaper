import requests
from datetime import datetime

class weatherData:
    user_api = "6aee7b32df66d715eb39a5015fa4eefe"

    def __init__(self):
        self.updateLoc()
        self.update()

    def update(self):
        api_link = requests.get(self.complete_api_link)
        api_data = api_link.json()
        self.temp = ((api_data['main']['temp']) - 273.15)
        self.weather_desc = api_data['weather'][0]['description']
        self.hmdt = api_data['main']['humidity']
        self.wind = api_data['wind']['speed']

    def updateLoc(self):
        locData = requests.get('https://extreme-ip-lookup.com/json')
        self.location = locData.json()['city']
        self.complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q="+self.location+"&appid="+self.user_api

    def getWindSpd(self):
        return ("{:.1f}".format(self.wind))

    def getTime(self):
        return datetime.now().strftime("%d %b %Y | %I:%M %p")

    def getTemp(self):
        return ("{:.1f}".format(self.temp))

    def getDescr(self):
        return self.weather_desc

    def getLoc(self):
        return self.location

w = weatherData()
print(w.getLoc(), w.getTemp(), w.getTime(), w.getWindSpd(), w.getDescr())