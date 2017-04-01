import pyowm

#class WeatherDataApi:

owm = pyowm.OWM('ecb73e81c510fd8cc1457529463be966')
observation = owm.weather_at_place("Cambridge,uk")
w = observation.get_weather()
wind = w.get_wind()

print(w)
print(wind)