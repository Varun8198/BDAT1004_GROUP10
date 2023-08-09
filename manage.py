#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import requests
import time
from pymongo import MongoClient

client = MongoClient('mongodb+srv://varun:oLNBSENvCEHeIBCr@group10.liamq4r.mongodb.net/?retryWrites=true&w=majority')
db = client.temperature
while True:

    url = requests.get(
        "https://api.open-meteo.com/v1/gem?latitude=60.1087&longitude=-113.6426&hourly=temperature_2m,relativehumidity_2m,apparent_temperature,surface_pressure,windspeed_10m,cape&daily=temperature_2m_max,temperature_2m_min&current_weather=true&timezone=auto&start_date=2023-08-06&end_date=2023-08-06")
    if url.status_code == 200:
        data = url.json()
        print(data)
        db.temperature.insert_one(data)
        time.sleep(25)
    else:
        exit()

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pythonProject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
