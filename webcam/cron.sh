#!/usr/bin/env bash

cd /home/pi/accvi-5040-hut/
source venv/bin/activate

./webcam/pull_image.sh
./webcam/rm_yesterday.sh
./webcam/latest_snowdepth.sh
./webcam/push_to_accvi.sh
./webcam/push_to_s3.sh
