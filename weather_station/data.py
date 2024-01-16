import dataclasses
from datetime import datetime, timedelta
from typing import List

from pyvantagepro import VantagePro2


class CurrentWeatherData(dict):
    # BarTrend:  # B
    # PacketType:  # B
    # Barometer:  # H
    # TempIn:  # H
    # HumIn:  # B
    # TempOut:  # H
    # WindSpeed:  # B
    # WindSpeed10Min:  # B
    # WindDir:  # H
    # ExtraTemps:  # 7s
    # SoilTemps:  # 4s
    # LeafTemps:  # 4s
    # HumOut:  # B
    # HumExtra:  # 7s
    # RainRate:  # H
    # UV:  # B
    # SolarRad:  # H
    # RainStorm:  # H
    # StormStartDate:  # H
    # RainDay:  # H
    # RainMonth:  # H
    # RainYear:  # H
    # ETDay:  # H
    # ETMonth:  # H
    # ETYear:  # H
    # SoilMoist:  # 4s
    # LeafWetness:  # 4s
    # AlarmIn:  # B
    # AlarmRain:  # B
    # AlarmOut:  # 2s
    # AlarmExTempHum:  # 8s
    # AlarmSoilLeaf:  # 4s
    # BatteryStatus:  # B
    # BatteryVolts:  # H
    # ForecastIcon:  # B
    # ForecastRuleNo:  # B
    # SunRise:  # H
    # SunSet:  # H

    def from_device(self, device: VantagePro2):
        data = device.get_current_data()
        return data


class ArchiveWeatherData(dict):
    # DateStamp     # H
    # TimeStamp     # H
    # TempOut       # H
    # TempOutHi     # H
    # TempOutLow    # H
    # RainRate      # H
    # RainRateHi    # H
    # Barometer     # H
    # SolarRad      # H
    # WindSamps     # H
    # TempIn        # H
    # HumIn         # B
    # HumOut        # B
    # WindAvg       # B
    # WindHi        # B
    # WindHiDir     # B
    # WindAvgDir    # B
    # UV            # B
    # ETHour        # B
    # SolarRadHi    # H
    # UVHi          # B
    # ForecastRuleNo # B
    # LeafTemps     # 2s
    # LeafWetness   # 2s
    # SoilTemps     # 4s
    # RecType       # B
    # ExtraHum      # 2s
    # ExtraTemps    # 3s
    # SoilMoist     # 4s

    @classmethod
    def from_device(cls, device: VantagePro2, start_date: datetime=None, end_date: datetime=None):
        if end_date is None:
            end_date = datetime.now()
        if start_date is None:
            start_date = datetime.now() - timedelta(days=7)

        data_list = device.get_archives(
            start_date=start_date,
            stop_date=end_date,
        )

        return [ArchiveWeatherData(
            **datum,
        ) for datum in data_list]
