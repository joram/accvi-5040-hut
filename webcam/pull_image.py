#!/usr/bin/env python3
import cv2
import os
import datetime
import dotenv

dotenv.load_dotenv()


def _filepath():
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    curr_dt = datetime.datetime.now().strftime("%Y-%M-%dT%H:%m:%s")
    filepath = os.path.join(curr_dir, f"../data/webcam/{curr_dt}.jpg")

    for dirname in [
        "../data",
        "../data/webcam",
    ]:
        fullpath = os.path.join(curr_dir, dirname)
        if not os.path.exists(fullpath):
            os.mkdir(fullpath)
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


if __name__ == "__main__":
    filepath = get_newest_image()
    print(filepath)

