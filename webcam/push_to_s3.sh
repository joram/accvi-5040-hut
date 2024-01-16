#!/usr/bin/bash
# This is meant to be run from the root of the project

# if there is no tar.gz files, exit
if [ ! "$(ls -A ./data/webcam/*.tar.gz)" ]; then
    echo "No files to send to S3"
    exit 0
fi

# if there is any tar.gz files, send them to s3
aws s3 mv --follow-symlinks ./data/webcam/*.tar.gz s3://5040-hut-data.oram.ca/webcam/  # Sync data to S3