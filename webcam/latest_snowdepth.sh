#!/usr/bin/env bash

#cd /home/pi/accvi-5040-hut/
source venv/bin/activate

LATEST_WEBCAM_IMAGE=$(find ./data/webcam -type f -printf '%T@ %p\n' | sort -n | tail -1 | awk '{print $2}')
echo "Latest webcam image: $LATEST_WEBCAM_IMAGE"
# Check if a .jpg file was found
if [[ -n "$LATEST_WEBCAM_IMAGE" ]]; then
  LATEST_SNOW_DEPTH_DEBUG_IMAGE="${LATEST_WEBCAM_IMAGE%.jpg}_snow_depth.jpg"
  LATEST_SNOW_DEPTH_DEBUG_TXT="${LATEST_WEBCAM_IMAGE%.jpg}_snow_depth.txt"
  ./webcam/snow_depth.py $LATEST_WEBCAM_IMAGE $LATEST_SNOW_DEPTH_DEBUG_IMAGE $LATEST_SNOW_DEPTH_DEBUG_TXT

  # Check if the snow depth image was created
  if [[ -f "$LATEST_SNOW_DEPTH_DEBUG_IMAGE" ]]; then
    echo "Snow depth image created: $LATEST_SNOW_DEPTH_DEBUG_IMAGE"
  else
    echo "Snow depth image not created."
  fi

else
    echo "No .jpg files found in the directory."
fi

