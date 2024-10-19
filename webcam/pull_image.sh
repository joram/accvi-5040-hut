#!/usr/bin/env bash

export $(grep -v '^#' .env | xargs -0)  # Load environment variables

TODAYS_DATE=$(date -d "today 13:00" '+%Y-%m-%d')
FILENAME=$(date -d "today 13:00" '+%Y-%m-%dT%H:%M:%S').jpg
cd /home/pi/accvi-5040-hut/data/webcam/$TODAYS_DATE

ffmpeg -y -i rtsp://${WEBCAM_USERNAME}:${WEBCAM_PASSWORD}@{WEBCAM_IP}:554/Streaming/Channels/101 -vframes 1 $FILENAME