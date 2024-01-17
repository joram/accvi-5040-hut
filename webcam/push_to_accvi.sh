#!/usr/bin/env bash

lastim=`ls -tr . | tail -1`
echo $lastim

scp  -i ${ID_RSA_FILEPATH} /home/pi/5040_hut_bastion/data/webcam/newest.jpg accvica@accvi.ca:www/wp-content/hutimages/newest.jpeg
