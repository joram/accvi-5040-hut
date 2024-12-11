#!/usr/bin/env bash

cd /home/pi/accvi-5040-hut/
export $(grep -v '^#' .env | xargs -0)  # Load environment variables

./weather_station/pull_weather.sh
./weather_station/push_s3.sh
