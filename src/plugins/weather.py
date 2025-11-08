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
    match = match_pattern.match(msg.clean_content)
    weatherResp = getWeather(match.groups()[0])
    if isinstance(weatherResp, dict):
        embed = Embed()
        embed.add_field(
            name="<:earth_africa:1424126880105238638> Location",
            value=weatherResp['location'],
            inline=True
        )
        embed.add_field(
            name="<:straight_ruler:1424128456136069150> Lat/Long",
            value=weatherResp['latlong'],
            inline=True
        )
        embed.add_field(
            name="☁ Condition",
            value=weatherResp['condition'],
            inline=True
        )
        embed.add_field(
            name="<:sweat:1424128456136069150> Humidity",
            value=weatherResp['humidity'],
            inline=True
        )
        embed.add_field(
            name="<:dash:1424128456136069150> Wind speed",
            value=weatherResp['windSpeed'],
            inline=True
        )
        embed.add_field(
            name="<:thermometer:1424128456136069150> Temperature",
            value=weatherResp['temperature'],
            inline=True
        )
        embed.add_field(
            name="<:high_brightness:1424128456136069150> Min/Max",
            value=weatherResp['minMax'],
            inline=True
        )
        embed.add_field(
            name="<:sunrise_over_mountains:1424128456136069150> Sunrise",
            value=weatherResp['sunrise'],
            inline=True
        )
        embed.add_field(
            name="<:city_sunset:1424128456136069150> Sunset",
            value=weatherResp['sunset'],
            inline=True
        )
        embed.set_footer(
            text="Powered by Nadeko uwu Kelbi-kun~~~~~",
            icon_url="https://openweathermap.org/img/w/04n.png"
        )
    else:
        embed = Embed(description=weatherResp)
    
    await msg.channel.send(embed=embed)