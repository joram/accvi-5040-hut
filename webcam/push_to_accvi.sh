#!/usr/bin/env bash

export $(grep -v '^#' .env | xargs -0)  # Load environment variables
cd /home/pi/accvi-5040-hut/data/webcam
lastimage=`ls -tr . | tail -1`
echo $lastimage
scp -i ${ID_RSA_FILEPATH} "$lastimage" accvica@accvi.ca:www/wp-content/hutimages/newest.jpeg
