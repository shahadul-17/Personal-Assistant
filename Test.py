# import pyowm
from Utility import Utility

'''from ResponseGenerator import ResponseGenerator
#class WeatherDataApi:

owm = pyowm.OWM('ecb73e81c510fd8cc1457529463be966')
observation = owm.weather_at_place("Dhaka, BD")
w = observation.get_weather()
wind = w.get_wind()

# print(w)
print(w.get_detailed_status())
# print(w.get_temperature('celsius'))
# print(wind)
print(w.get_humidity())

# print(owm.is_API_online())
'''
# print(Utility.__getValueFromFile(".\\configuration.ini", port))

print(Utility.getData('hello', Utility.getDataFrame("response.xlsx")))