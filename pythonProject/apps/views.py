import time

import requests
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
from django.http import JsonResponse
import json
import datetime

def IndexView(request):
    template_name = 'index.html'
    client = MongoClient('mongodb+srv://varun:oLNBSENvCEHeIBCr@group10.liamq4r.mongodb.net')
    db = client.temperature
    data = list(db.temperature.find().limit(5))
    dataArr = [["Date", "Temperature " + data[0]["hourly_units"]["temperature_2m"], "Humidity" + data[0]["hourly_units"]["relativehumidity_2m"]]]
    dataBar=[["Date", "Min Temperature " + data[0]["hourly_units"]["temperature_2m"], "Max Temperature " + data[0]["hourly_units"]["temperature_2m"]]]
    for index in range(len(data[0]["hourly"]["time"])):
        dateObj = datetime.datetime.strptime(data[0]["hourly"]["time"][index], "%Y-%m-%dT%H:%M")
        dataArr.append([dateObj.strftime("%m-%d-%Y %H: %M"),data[0]["hourly"]["temperature_2m"][index],data[0]["hourly"]["relativehumidity_2m"][index]])


    data = list(db.temperature.find())
    for index in range(len(data)):
        dateObj = datetime.datetime.strptime(data[index]["daily"]["time"][0], "%Y-%m-%d")
        dataBar.append([dateObj.strftime("%m-%d-%Y"), data[index]["daily"]["temperature_2m_min"][0],
                        data[index]["daily"]["temperature_2m_max"][0]])

    args = {}
    args['dataset'] = mark_safe(json.dumps(dataArr))
    args['datasetBar'] = mark_safe(json.dumps(dataBar))
    return TemplateResponse(request, template_name, args)

def GetAllItems(request):
    client = MongoClient('mongodb+srv://varun:oLNBSENvCEHeIBCr@group10.liamq4r.mongodb.net')
    db = client.temperature
    data = db.temperature.find()
    return JsonResponse(dumps(data), safe=False)

def GetItemById(request):
    client = MongoClient('mongodb+srv://varun:oLNBSENvCEHeIBCr@group10.liamq4r.mongodb.net')
    db = client.temperature
    data = db.temperature.find({"_id": ObjectId(request.GET["id"])})
    return JsonResponse(dumps(data), safe=False)

def GetRangeItems(request):
    client = MongoClient('mongodb+srv://varun:oLNBSENvCEHeIBCr@group10.liamq4r.mongodb.net')
    db = client.temperature
    data = db.temperature.find({"daily.time":{"$gte": request.GET["fromDate"], "$lte": request.GET["toDate"]}})
    return JsonResponse(dumps(data), safe=False)

def LoadDataIntoDB(request):
    client = MongoClient(
        'mongodb+srv://varun:oLNBSENvCEHeIBCr@group10.liamq4r.mongodb.net/?retryWrites=true&w=majority')
    db = client.temperature
    now = datetime.datetime.now()
    nowStr = now.strftime("%Y-%m-%d")
    while True:
        url = requests.get(
            "https://api.open-meteo.com/v1/gem?latitude=60.1087&longitude=-113.6426&hourly=temperature_2m,relativehumidity_2m,apparent_temperature,surface_pressure,windspeed_10m,cape&daily=temperature_2m_max,temperature_2m_min&current_weather=true&timezone=auto&start_date="+nowStr+"&end_date="+nowStr)
        if url.status_code == 200:
            data = url.json()
            print(data)
            db.temperature.insert_one(data)
            time.sleep(86400)
        else:
            exit()