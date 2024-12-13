#!/usr/bin/bash
# This is meant to be run from the root of the project
export $(grep -v '^#' .env | xargs -0)  # Load environment variables

# push jpg files to S3 (resume failed previous pushes)
TODAYS_DATE=$(date -d "today 13:00" '+%Y-%m-%d')
cd /home/pi/accvi-5040-hut/data/webcam/$TODAYS_DATE
aws s3 sync --follow-symlinks . s3://5040-hut-data.oram.ca/wea/$TODAYS_DATE/