import pyowm

from datetime import datetime
from Utility import Utility

class Weather:

    _owm = None

    def __init__(self):
        self._owm = pyowm.OWM(Utility.getValueFromConfigurationFile("open-weather-api-key"))
    
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
        return datetime.fromtimestamp(self.__getWeather(location).get_sunrise_time()).strftime(Utility.getValueFromConfigurationFile("time-format"))
    
    def getSunsetTime(self, location):
        return datetime.fromtimestamp(self.__getWeather(location).get_sunset_time()).strftime(Utility.getValueFromConfigurationFile("time-format"))

    def getHumidity(self, location):
        return 'Humidity is ' + str(self.__getWeather(location).get_humidity()) + '%'
    
    def getWindInformation(self, location):       # needs to be fixed...
        i = 0
        temp = None
        direction = None
        speed = None
        windInformation = str(self.__getWeather(location).get_wind())
        _list = windInformation.split(', ')

        for item in _list:
            if i == 0:
                temp = "'deg': "
            else:
                temp = "'speed': "
            
            item = item[item.rfind(temp) + len(temp):]

            if i == 0:
                direction = item
            else:
                speed = item[: len(item) - 1]
            
            i += 1
        
        return 'direction = ' + direction + ' and speed = ' + speed + ' meters per second'

        # return 'Wind is blowing due ' + 
        # "the wind is blowing due north."