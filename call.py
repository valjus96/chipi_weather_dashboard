#ChiPi Weather Dashboard
#By valjus96, (https://github.com/valjus96)

#OpenWeather call module.

import requests

class Api_call():
    def __init__(self):
        self.__url = "http://api.openweathermap.org/data/2.5/weather?appid="
        self.__forecast_url = "http://api.openweathermap.org/data/2.5/forecast?q="

    def call_api(self, api_key="", location="Seinäjoki", forecasts=False):
        
        if forecasts == False:
            response = requests.get(self.__url + api_key + "&q=" + location, timeout=5)
            if response.status_code != 200:
                return None
        else:
            response = requests.get(self.__forecast_url + location + "&appid=" + api_key, timeout=5)
            if response.status_code != 200:
                 return None

        data = response.json()
        return data

def create_obj():
    return Api_call()


