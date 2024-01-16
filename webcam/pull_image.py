#!/usr/bin/env python3
import cv2
import urllib.request
import numpy as np
import os
import datetime


def _filepath():
    curr_dir = os.path.realpath(__file__)
    curr_dt = datetime.datetime.now().strftime("%y-%M-%DT%h:%m:%s")
    filepath = os.path.join(curr_dir, f"../data/{curr_dt}.jpg")
    os.mkdirs(os.path.dirname(filepath), exist_ok=True)
    return filepath


def get_newest_image():
    username = os.environ.get("WEBCAM_USERNAME")
    password = os.environ.get("WEBCAM_PASSWORD")
    ip = os.environ.get("WEBCAM_IP")
    filepath = _filepath()

    rtsp_url = f"rtsp://{username}:{password}@{ip}:554/h265Preview_01_main"
    cap = cv2.VideoCapture(rtsp_url)
    ret, frame = cap.read()
    cv2.imwrite(filepath, frame)

    return filepath


def update_symbolic_link(filepath):
    symlink_path = os.path.join(os.path.dirname(filepath), "newest.jpg")
    os.symlink(filepath, symlink_path, target_is_directory=False)


if __name__ == "__main__":
    filepath = get_newest_image()
    update_symbolic_link(filepath)
