#!/usr/bin/env bash

cd /home/pi/5040_hut_bastion/
export $(grep -v '^#' .env | xargs -0)  # Load environment variables
source venv/bin/activate

./webcam/pull_image.sh
./webcam/push_to_accvi.sh
./webcam/compress_yesterday.sh
./webcam/push_to_s3.sh
