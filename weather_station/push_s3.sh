#!/usr/bin/bash
# This is meant to be run from the root of the project

export $(grep -v '^#' .env | xargs -0)  # Load environment variables
aws s3 mv --follow-symlinks ./data/weather_station/ s3://5040-data.oram.ca/weather_station/  # Sync data to S3
