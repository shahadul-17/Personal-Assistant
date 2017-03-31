import pyowm

from datetime import datetime
from Utilities import Utilities

class Weather:

    _owm = None

    def __init__(self):
        self._owm = pyowm.OWM(Utilities.getValueFromConfigurationFile("open-weather-api-key"))
    
    def __getWeather(self, location):
        return self._owm.weather_at_place(location).get_weather()

    def getWeatherStatus(self, location):
        return "It's " + self.__getWeather(location).get_detailed_status()
    
    def __getTemperature(self, weather, temperatureUnit):
        temp = "'temp': "
        temperature = str(weather.get_temperature(temperatureUnit.lower()))
        _list = temperature.split(', ')
        temperature = None

        for item in _list:
            if item.__contains__(temp):
                temperature = item[item.rfind(temp) + len(temp):]

                break
        
        return temperature + " degree " + temperatureUnit
    
    def getTemperature(self, location):
        i = 0
        temperature = "It's "
        temperatureUnits = [ 'Celsius', 'Fahrenheit' ]

        for temperatureUnit in temperatureUnits:
            temperature += self.__getTemperature(self.__getWeather(location), temperatureUnit)

            if i == 0:
                i += 1
                temperature += ' or '
        
        return temperature
    
    def getSunriseTime(self, location):
        return datetime.fromtimestamp(self.__getWeather(location).get_sunrise_time()).strftime("%I:%M %p")
    
    def getHumidity(self, location):
        return 'Humidity is ' + str(self.__getWeather(location).get_humidity()) + '%'