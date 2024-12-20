#!/usr/bin/env bash

export $(grep -v '^#' .env | xargs -0)  # Load environment variables

TODAYS_DATE=$(date -d "today 13:00" '+%Y-%m-%d')
mkdir -p /home/pi/accvi-5040-hut/data/webcam/$TODAYS_DATE
cd /home/pi/accvi-5040-hut/data/webcam/$TODAYS_DATE

ffmpeg -rtsp_transport tcp -buffer_size 1024000 -i rtsp://${WEBCAM_USERNAME}:${WEBCAM_PASSWORD}@192.168.99.207:554/Streaming/Channels/101 -frames:v 1 -q:v 2 -strftime 1 "%Y-%m-%dT%H-%M-%S.jpg"
