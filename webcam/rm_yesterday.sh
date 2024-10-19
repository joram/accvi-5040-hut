#!/usr/bin/env bash

YESTERDAYS_DATE=$(date -d "yesterday 13:00" '+%Y-%m-%d')
YESTERDAYS_FOLDER="/home/pi/5040_hut_bastion/data/webcam/$YESTERDAYS_DATE"
YESTERDAYS_FOLDER="./data/webcam/$YESTERDAYS_DATE"

if [ -d "$YESTERDAYS_FOLDER" ]; then
    echo "Removing $YESTERDAYS_FOLDER"
    rm -rf "$YESTERDAYS_FOLDER"
else
    echo "No folder found for $YESTERDAYS_DATE"
fi
