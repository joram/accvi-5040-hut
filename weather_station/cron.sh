#!/usr/bin/env bash
./pull_data.sh
./push_s3.sh
./push_wunderground.sh
./purge_data.sh