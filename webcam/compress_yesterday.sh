#!/usr/bin/env bash

# This is meant to be run from the root of the project
# looking at yesterday's folder of data, if a folder exists for yesterday:
#    - compress it to a tar.gz file in the data/$Y-$m-$d.tar.gz format
#    - then delete the folder

YESTERDAYS_DATE=$(date -d "yesterday 13:00" '+%Y-%m-%d')
YESTERDAYS_FOLDER="/home/pi/5040_hut_bastion/data/webcam/$YESTERDAYS_DATE"
YESTERDAYS_FOLDER="./data/webcam/$YESTERDAYS_DATE"

if [ -d "$YESTERDAYS_FOLDER" ]; then
    echo "Compressing $YESTERDAYS_FOLDER"
    tar -czf "$YESTERDAYS_FOLDER.tar.gz" --directory="$YESTERDAYS_FOLDER" .
    rm -rf "$YESTERDAYS_FOLDER"
else
    echo "No folder found for $YESTERDAYS_DATE"
fi
