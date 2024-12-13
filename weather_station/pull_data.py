#!/usr/bin/env python3
from pyvantagepro import VantagePro2
import csv
import json
from io import StringIO

url = "serial:/dev/ttyUSB0:19200:8N1"
device = VantagePro2.from_url(url)
csv_data = device.get_current_data().to_csv()
csv_file = StringIO(csv_data)
reader = csv.DictReader(csv_file)
json_data = {}
for d in reader:
    json_data = d

print(json_data)
