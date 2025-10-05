import datetime
import json
import os
import re
import urllib
from ..utils import querify
from discord import Embed

trigger = re.compile("^!we")
keywords = ["we", "weather"]

match_pattern = re.compile(r"^!we\s+(.+)")
baseURL = 'https://api.openweathermap.org/data/2.5/weather'

openweathermapAPIKey = json.load(open(os.path.abspath(os.path.dirname(__file__) + "/weather.json")))['key']


def kelvinToCelsius(tempKel):
    return round(tempKel - 273.15, 1)

def kelvinToFahrenheit(tempKel):
    return round((tempKel - 273.15) * (9/5) + 32, 1)

def getWeather(place):
    params = {
        "q": place,
        "appid": openweathermapAPIKey
    }
    try:
        response = urllib.request.urlopen(baseURL + querify(params)).read()
    except urllib.error.HTTPError as err:
        print("OpenWeatherMap request failed: %s - Returning City not found response" % err)
        return 'City not found'
    else:
        try:
            parsed = json.loads(response.decode("utf-8"))
        except json.JSONDecodeError as err:
            print("Failed to parse OpenWeatherMap response: %s" % err)
        else:
            if isinstance(parsed, dict):
                weather = {}
                weather['location'] = "[" + parsed['name'] + ", " + parsed['sys']['country'] + "](https://openweathermap.org/city/" + str(parsed['id']) + ")"
                weather['latlong'] = str(parsed['coord']['lat']) + ", " + str(parsed['coord']['lon'])
                weather['condition'] = parsed['weather'][0]['main']
                weather['humidity'] = str(parsed['main']['humidity']) + '%'
                weather['windSpeed'] = str(parsed['wind']['speed']) + ' m/s'
                weather['temperature'] = str(kelvinToCelsius(parsed['main']['temp'])) + "°C / " + str(kelvinToFahrenheit(parsed['main']['temp'])) + "°F"
                weather['minMax'] = str(kelvinToCelsius(parsed['main']['temp_min'])) + "°C - " \
                    + str(kelvinToCelsius(parsed['main']['temp_max'])) + "°C\n" \
                    + str(kelvinToFahrenheit(parsed['main']['temp_min'])) + "°F - " \
                    + str(kelvinToFahrenheit(parsed['main']['temp_max'])) + "°F"
                weather['sunrise'] = datetime.datetime.fromtimestamp(parsed['sys']['sunrise'], tz=datetime.timezone.utc).strftime('%H:%M %Z%z')
                weather['sunset'] = datetime.datetime.fromtimestamp(parsed['sys']['sunset'], tz=datetime.timezone.utc).strftime('%H:%M %Z%z')
                return weather                    

async def action(bot, msg):
    weatherResp = getWeather(msg.clean_content)
    embed = Embed()
    if isinstance(weatherResp, dict):
        embed.add_field(
            "<:earth_africa:1424126880105238638> Location",
            weatherResp['location'],
            True
        )
        embed.add_field(
            "<:straight_ruler:1424128456136069150> Lat/Long",
            weatherResp['latlong'],
            True
        )
        embed.add_field(
            "☁ Condition",
            weatherResp['condition'],
            True
        )
        embed.add_field(
            "<:sweat:1424128456136069150> Humidity",
            weatherResp['humidity'],
            True
        )
        embed.add_field(
            "<:dash:1424128456136069150> Wind speed",
            weatherResp['windSpeed'],
            True
        )
        embed.add_field(
            "<:thermometer:1424128456136069150> Temperature",
            weatherResp['temperature'],
            True
        )
        embed.add_field(
            "<:high_brightness:1424128456136069150> Min/Max",
            weatherResp['minMax'],
            True
        )
        embed.add_field(
            "<:sunrise_over_mountains:1424128456136069150> Sunrise",
            weatherResp['sunrise'],
            True
        )
        embed.add_field(
            "<:city_sunset:1424128456136069150> Sunset",
            weatherResp['sunset'],
            True
        )
        embed.set_footer(
            "Powered by Nadeko uwu Kelbi-kun~~~~~",
            "https://openweathermap.org/img/w/04n.png"
        )
    else:
        embed.description(weatherResp)
    
    await bot.send_message(msg.channel, embed=embed)
