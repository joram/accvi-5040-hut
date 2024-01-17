#!/usr/bin/env bash

cd /home/pi/accvi-5040-hut/data/webcam
lastim=`ls -tr . | tail -1`
echo $lastim

scp  -i ${ID_RSA_FILEPATH} /home/pi/accvi-5040-hut/data/webcam/newest.jpg accvica@accvi.ca:www/wp-content/hutimages/newest.jpeg
