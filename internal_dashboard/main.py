#!/usr/bin/env python3
import requests
import json
import os
from datetime import datetime
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles

from fastapi.responses import FileResponse
import uvicorn


app = FastAPI()

#  static files
curr_dir = os.path.dirname(os.path.realpath(__file__))
static_dir = os.path.join(curr_dir, "static")
data_dir = os.path.join(curr_dir, "../data")
app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")

# def _cache_images(data):
#     images = data.get("media", {}).get("images", [])
#     for image in images:
#         url = image.get("url")
#         response = requests.get(url)
#         filename = url.split("/")[-1]
#         with open(f"./data/website/{filename}", 'wb') as f:
#             f.write(response.content)


def get_avi_report():
    now = datetime.now()
    cache_file = f"{data_dir}/website/{now.strftime('%Y-%m-%d')}/{now.strftime('%Y-%m-%dT%H')}_avi_report.json"
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)

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
    return FileResponse("./static/index.html")

@app.get("/avi_report")
def read_avi_report():
    data = get_avi_report()
    return data

@app.get("/weather_forecast")
def read_weather_forecast():
    data = get_weather_forecast()
    return data

if __name__ == "__main__":
    get_weather_forecast()
    uvicorn.run("main:app", host="0.0.0.0", port=5040, reload=True)
