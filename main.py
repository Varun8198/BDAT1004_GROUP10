import requests
import time
from pymongo import MongoClient
import datetime

client = MongoClient('mongodb+srv://varun:oLNBSENvCEHeIBCr@group10.liamq4r.mongodb.net/?retryWrites=true&w=majority')
db = client.temperature
now = datetime.datetime.now()
nowStr = now.strftime("%Y-%m-%d")
while True:

    url = requests.get("https://api.open-meteo.com/v1/gem?latitude=60.1087&longitude=-113.6426&hourly=temperature_2m,relativehumidity_2m,apparent_temperature,surface_pressure,windspeed_10m,cape&daily=temperature_2m_max,temperature_2m_min&current_weather=true&timezone=auto&start_date="+nowStr+"&end_date="+nowStr)
    if url.status_code == 200:
        data = url.json()
        print(data)
        db.temperature.insert_one(data)
        time.sleep(86400)
    else:
        exit()