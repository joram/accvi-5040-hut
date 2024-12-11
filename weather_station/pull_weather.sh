#!/usr/bin/env bash
DATE_TIMESTAMP=$(date +"%Y-%m-%d")
TIMESTAMP=$(date +"%Y-%m-%dT%H:%M:%S")
OUTPUT_DIR=./data/weather_station/${DATE_TIMESTAMP}
OUTPUT_FILE=${OUTPUT_DIR}/${TIMESTAMP}.json

mkdir -p ${OUTPUT_DIR}
ssh 192.168.99.22  "python3 ./get_wx_data.py" > ${OUTPUT_FILE}

