#!/usr/bin/env python3

import datetime
import os

import requests

from .pull_data import get_weather_data

STATION_ID = os.environ.get("WUNDERGROUND_STATION_ID")
STATION_KEY = os.environ.get("WUNDERGROUND_STATION_KEY")
API_ENDPOINT = 'https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php'


def _push_weather(
    humidity=None,
    barometer_in=None,
    wind_speed_mph=None,
    wind_gust_mph=None,
    temp_f=None,
    rain_in=None,
    soil_temp_f=None,
    wind_dir=None,
):

    payload = {
        'ID': STATION_ID,
        'PASSWORD': STATION_KEY,
        'dateutc': str(datetime.datetime.utcnow()),
        'action': 'updateraw',
    }
    for (key, value) in [
        ("humidity", humidity),
        ("baromin", barometer_in),
        ("windspeedmph", wind_speed_mph),
        ("windgustmph", wind_gust_mph),
        ("tempf", temp_f),
        ("rainin", rain_in),
        ("soiltempf", soil_temp_f),
        ("winddir", wind_dir),
    ]:
        if value is not None:
            payload[key] = value

    response = requests.get(API_ENDPOINT, params=payload)
    print(response.text)


def push_weather():
    data = get_weather_data()
    _push_weather(
        humidity=data.get("HumOut"),
        barometer_in=data.get("Barometer"),
        wind_speed_mph=data.get("WindSpeed"),
        wind_gust_mph=data.get("WindSpeed10Min"),
        temp_f=data.get("TempOut"),
        rain_in=data.get("RainDay"),
        soil_temp_f=data.get("SoilTemps", [None])[0],
        wind_dir=data.get("WindDir"),
    )


if __name__ == '__main__':
    push_weather()
