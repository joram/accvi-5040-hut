#!/usr/bin/env python3
import requests
import json
import os
from datetime import datetime
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles

from fastapi.responses import FileResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  static files
curr_dir = os.path.dirname(os.path.realpath(__file__))
static_dir = os.path.join(curr_dir, "dist/assets")
data_dir = os.path.join(curr_dir, "../data")
app.mount("/assets", StaticFiles(directory=static_dir, html=True), name="static")

def _current_cache_filepath(name: str) -> str:
    now = datetime.now()
    filepath = f"{data_dir}/{now.strftime('%Y-%m-%d')}/{now.strftime('%Y-%m-%dT%H')}_{name}.json"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    return filepath


def get_avi_report():
    cache_file = _current_cache_filepath("avi_report")

    # Check if the data is cached
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            data = json.load(f)
        return data

    product_id = None
    url = "https://api.avalanche.ca/forecasts/en/products"
    response = requests.get(url)
    data = response.json()
    for product in data:
        title = product["report"]["title"]
        if "island" in title.lower():
            product_id = product["id"]
            break


    # If the data is not cached, fetch it from the API
    url = f"https://api.avalanche.ca/forecasts/en/products/{product_id}"
    response = requests.get(url)
    data = response.json()
    with open(cache_file, 'w') as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))
    # _cache_images(data)

    return data


def get_weather_forecast():

    now = datetime.now()
    cache_file = f"{data_dir}/website/{now.strftime('%Y-%m-%d')}/{now.strftime('%Y-%m-%dT%H')}_weather_forecast.json"
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)

    # Check if the data is cached
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            data = json.load(f)
        return data

    # If the data is not cached, fetch it from the API
    url = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=49.18916667&lon=-125.2875&altitude=1350"
    response = requests.get(url, headers={"User-Agent": "ACCVI-hut2"})
    if response.status_code != 200:
        print(response.text)
    data = response.json()
    with open(cache_file, 'w') as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))

    return data


@app.get("/")
def read_root():
    return FileResponse("./dist/index.html")


@app.get("/api/avalanche_forecast")
def read_avi_report():
    data = get_avi_report()
    return data


@app.get("/api/weather_forecast")
def read_weather_forecast():
    data = get_weather_forecast()
    return data

@app.get("/api/weather_history")
def read_weather_history():
    url = "https://s3.ca-central-1.amazonaws.com/5040-hut-data.oram.ca/weather_station/summary.json"
    cache_file = _current_cache_filepath("weather_history")

    # Check if the data is cached
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            data = json.load(f)
        return data

    # If the data is not cached, fetch it from the API
    response = requests.get(url)
    data = response.json()

    # Save the data to the cache
    with open(cache_file, 'w') as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))

    return data


@app.get("/api/snow_depth")
def read_snow_depth():
    url = "https://s3.ca-central-1.amazonaws.com/5040-hut-data.oram.ca/snow_depth/summary.json"
    cache_file = _current_cache_filepath("snow_depth")

    # Check if the data is cached
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            data = json.load(f)
        return data

    # If the data is not cached, fetch it from the API
    response = requests.get(url)
    data = response.json()

    # Save the data to the cache
    with open(cache_file, 'w') as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))

    return data

@app.get("/api/webcam/todays_images")
def read_webcam_image_list():
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    bucketUrl = f"https://s3.ca-central-1.amazonaws.com/5040-hut-data.oram.ca/?prefix=webcam/{year}-{month}-{day}/"
    print(bucketUrl)

    response = requests.get(bucketUrl)
    data = response.text
    import re
    files = re.findall(r'<Key>(.*?)</Key>', data)
    print(files)
    return {
        "todays_images": files
    }

@app.get("/api/webcam/key/{filename}")
def read_webcam_image(filename):
    if os.path.exists(f"{data_dir}/webcam/{filename}"):
        return FileResponse(f"{data_dir}/webcam/{filename}")


    ymd = filename.split("T")[0]
    url = f"https://s3.ca-central-1.amazonaws.com/5040-hut-data.oram.ca/webcam/{ymd}/{filename}"
    print(url)

    response = requests.get(url)
    with open(f"{data_dir}/webcam/{filename}", 'wb') as f:
        f.write(response.content)
    return FileResponse(f"{data_dir}/webcam/{filename}")

if __name__ == "__main__":
    get_weather_forecast()
    uvicorn.run("main:app", host="0.0.0.0", port=5040, reload=True)
