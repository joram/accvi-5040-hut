#!/usr/bin/env bash

cd /home/pi/accvi-5040-hut/
source venv/bin/activate

./webcam/pull_image.py
./webcam/push_to_accvi.sh
./webcam/compress_yesterday.sh
#./webcam/push_to_s3.sh
