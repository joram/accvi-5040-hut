#!/usr/bin/env bash

cd /home/pi/5040_hut_bastion/
export $(grep -v '^#' .env | xargs -0)  # Load environment variables

./pull_data.sh
./push_s3.sh
