#!/usr/bin/env python3

import sys
import argparse
import requests
from unidecode import unidecode
#from geolocateme import Geolocator
import jinja2

# OpenWeatherMap API key
appid = "<ENTER YOUR API KEY>"

# define icons
#  icons = {
#      'clear': "",
#      'clouds': "",
#      'rain': "",
#      'thunderstorm': "",
#      'snow': "",
#      'fog': ""
#  }

icons = {
    # clear
    800: '', # clear sky

    # clouds
    801: '', # few clouds: 11-25%
    802: '', # scattered clouds: 25-50%
    803: '', # broken clouds: 51-84%
    804: '', # overcast clouds: 85-100%

    # drizzle
    300: '', # light intensity drizzle
    301: '', # drizzle
    302: '', # heavy intensity drizzle
    310: '', # light intensity drizzle rain
    311: '', # drizzle rain
    312: '', # heavy intensity drizzle rain
    313: '', # shower rain and drizzle
    314: '', # heavy shower rain and drizzle
    321: '', # shower drizzle

    # rain
    500: '', # light rain
    501: '', # moderate rain
    502: '', # heavy intensity rain
    503: '', # very heavy rain
    504: '', # extreme rain
    511: '', # freezing rain
    520: '', # light intensity shower rain
    521: '', # shower rain
    522: '', # heavy intensity shower rain
    531: '', # ragged shower rain

    # thunderstorm
    200: '', # thunderstorm with light rain
    201: '', # thunderstorm with rain
    202: '', # thunderstorm with heavy rain
    210: '', # light thunderstorm
    211: '', # thunderstorm
    212: '', # heavy thunderstorm
    221: '', # ragged thunderstorm
    230: '', # thunderstorm with light drizzle
    231: '', # thunderstorm with drizzle
    232: '', # thunderstorm with heavy drizzle

    # snow
    600: '', # light snow
    601: '', # Snow
    602: '', # Heavy snow
    611: '', # Sleet
    612: '', # Light shower sleet
    613: '', # Shower sleet
    615: '', # Light rain and snow
    616: '', # Rain and snow
    620: '', # Light shower snow
    621: '', # Shower snow
    622: '', # Heavy shower snow

    # atmosphere
    701: '', # mist
    711: '', # smoke
    721: '', # haze
    731: '', # sand/dust whirls
    741: '', # fog
    751: '', # sand
    761: '', # dust
    762: '', # volcanic ash
    771: '', # sqalls
    781: '', # tornado
}

class _WeatherInfo():
    def __init__(self, raw_json_data):
        raw_weather = raw_json_data["weather"][0]
        raw_main = raw_json_data["main"]

        self._condition_id = raw_weather["id"]
        self.description_short = raw_weather["main"].lower()
        self.description_long = raw_weather["description"]
        self.temperature = raw_main["temp"]
        self.temperature_min = raw_main["temp_min"]
        self.temperature_max = raw_main["temp_max"]
        self.pressure = raw_main["pressure"]
        self.humidity = raw_main["humidity"]
        self.icon = icons[self._condition_id]

    def __getitem__(self, item):
         return getattr(self, item)


class WeatherMan(object):
    def __init__(self, owm_api_key, city_id = None, lat = None, lon = None, units = 'metric'):
        self._api_key = owm_api_key
        self._units = units

        self._city_id = city_id
        self._gps = (lat,lon)

        self.city = ""
        self.current = None
        self.next = None

        if self._city_id is None and (self._gps[0] is None or self._gps[1] is None):
            coor = Geolocator().get_location()
            self._gps = (coor.latitude, coor.longitude)

        self._get_weather()

    def _get_weather(self):
        params = {
            'units': self._units,
            'appid': self._api_key,
        }

        if self._city_id is not None:
            params['id'] = self._city_id
        else:
            params['lat'] = self._gps[0]
            params['lon'] = self._gps[1]

        r = requests.get(
            "http://api.openweathermap.org/data/2.5/forecast", params=params)
        d = r.json()

        if d['cod'] != '200':
            raise Exception("cannot get weather forecast", d['message'])

        self.city = d["city"]["name"]
        self._city_id = d["city"]["id"] if self._city_id is None else self._city_id
        self.current = _WeatherInfo(d["list"][0])
        self.next = _WeatherInfo(d["list"][1])

    def __getitem__(self, item):
         return getattr(self, item)


def main(city_id, lat, lon, template):
    weather = WeatherMan(appid, city_id, lat, lon)
    t = jinja2.Template(template)
    print(t.render(city = weather.city, current = weather.current, next = weather.next))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        add_help=True, description='Print weather informations for a location')

    parser.add_argument("--lat", action="store", dest="lat",
                        default=None, help="GPS latitude")
    parser.add_argument("--lon", action="store", dest="lon",
                        default=None, help="GPS longitude")
    parser.add_argument("--city-id", action="store", dest="city_id",
                        default=None, help="City ID by OpenWeatherMap")
    parser.add_argument("--output-format", action="store", dest="output_format",
                        default="{{city}} - {{current.description_long}} - {{current.temperature}}°C", help="Output format jinja template")

    try:
        args = parser.parse_args()
    except SystemExit as exception:
        print(exception)
    args, unknown = parser.parse_known_args()

    #  if (args.city_id != 0 and (args.lat != 0 or args.lon != 0)) or ((args.lat != 0 and args.lon == 0) or (args.lat == 0 and args.lon != 0)):
    #      print("Invalid parameters")
    #      sys.exit(1)

    main(args.city_id, args.lat, args.lon, args.output_format)

