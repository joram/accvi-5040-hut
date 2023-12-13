#!/usr/bin/env python3
import dataclasses
import datetime
import json
import os.path
from typing import List

from pyvantagepro import VantagePro2

from data import CurrentWeatherData, ArchiveWeatherData

STATION_URL = "tcp:192.168.99.23:1111"


class WeatherStationSnapshot(dataclasses.dataclass):
    unix_timestamp: int
    firmware_version: str
    time: datetime.datetime
    current_data: CurrentWeatherData
    archives: List[ArchiveWeatherData]


def get_weather_data() -> WeatherStationSnapshot:
    device = VantagePro2.from_url(STATION_URL)
    now = datetime.datetime.now()
    return WeatherStationSnapshot(
        time=now,
        unix_timestamp=now.timestamp(),
        firmware_version=device.firmware_version(),
        current_data=CurrentWeatherData.from_device(device),
        archives=ArchiveWeatherData.from_device(device),
    )


def get_filepath():
    now = datetime.datetime.now()
    now_str = now.strftime("%m/%d/%Y, %H:%M:%S")
    current_path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_path, f"../data/weather_station/{now_str}.json")
    fullpath = os.path.abspath(filepath)
    if not os.path.exists(fullpath):
        os.makedirs(fullpath)
    return filepath


def write_weather_data_to_file():
    try:
        details = get_weather_data()
    except Exception as e:
        details = {"error": str(e)}

    filepath = get_filepath()
    with open(filepath, "w") as f:
        f.write(json.dumps(details, indent=4, sort_keys=True))


if __name__ == "__main__":
    write_weather_data_to_file()
