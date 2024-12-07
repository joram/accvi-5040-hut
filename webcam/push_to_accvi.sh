#!/usr/bin/env bash

export $(grep -v '^#' .env | xargs -0)  # Load environment variables
TODAYS_DATE=$(date -d "today 13:00" '+%Y-%m-%d')
cd /home/pi/accvi-5040-hut/data/webcam/$TODAYS_DATE
lastimage=$(find . -type f ! -name '*_snow_depth.jpg' ! -name '*.txt' -exec stat -c "%Y %n" {} + 2>/dev/null | sort -n | tail -n 1 | cut -d' ' -f2-)

echo $lastimage
scp -i ${ID_RSA_FILEPATH} "./$lastimage" accvica@accvi.ca:www/wp-content/hutimages/newest.jpeg
