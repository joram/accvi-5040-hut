#!/usr/bin/bash
# This is meant to be run from the root of the project

export $(grep -v '^#' .env | xargs -0)  # Load environment variables
aws s3 sync --follow-symlinks ./data/ s3://5040.oram.ca  # Sync data to S3
