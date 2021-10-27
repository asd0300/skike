import time,os
import requests
import json
from env import param
from pymongo import MongoClient
import concurrent.futures
import pipelinesample
from env import config


# ###date generator
# from datetime import date, timedelta

# def daterange(start_date, end_date):
#     for n in range(int((end_date - start_date).days)):
#         yield start_date + timedelta(n)
# ####
# print(os.getcwd())
with open(r"C:\Users\Ben Fan\Desktop\Main_20211013_project\hotel_sample.json",encoding="utf-8") as f:
    i= json.load(f)
hotelList = i['accommodations']
for hotel in hotelList[0:2]:
    hotelName = hotel['name']['value']
    hotelType = hotel['accommodationCategory']
    hotelLocality = hotel['locality']['value']
    hotelMPic=hotel['images']['mainUri']
    hotelPic2=hotel['images']['retinaMainUri']
    likeBaseOn = hotel['rating']['basedOn']
    overallLike = hotel['rating']['formattedOverallLiking']
    hotelgeocodelat = hotel['geocode']['lat']
    hotelgeocodelng = hotel['geocode']['lng']
    dealAgent = hotel['deals']['bestPrice']['name']['value']
    disprice = hotel['deals']['bestPrice']['pricePerStay']
    # alterChoceName = 
    if hotel['conceptDistance']!=None:
        hotelMRT = hotel['conceptDistance'][0]['name']['value']
        print("hotelMRT "+hotelMRT)
    else:
        print("hotelMRT "+"null")
    # print(hotel)
    print(hotelName,hotelType,hotelLocality,hotelMPic,hotelPic2,hotelgeocodelat,hotelgeocodelng,disprice)
    print("------------------------------------------------------------------------------------")



# lowPrice = i["lowestPrice"]
# durationHour = i["productInfoList"][0]["durationInfo"]['hour'] #int 20
# durationMin = i["productInfoList"][0]["durationInfo"]['min'] #int 5
# avbTickets = i["productInfoList"][0]["avbTickets"] #int 9
# dDateTime = i["productInfoList"][0]["dDateTime"] #int 1641300000
# aDateTime = i["productInfoList"][0]["aDateTime"] #1641375900
# filterInfoListdtime = i["productInfoList"][0]["filterInfoList"][0]['dTimeStr'] #str
# filterInfoListatime = i["productInfoList"][0]["filterInfoList"][0]['aTimeStr']+"+{}d".format(str(i["productInfoList"][0]['arrivalDays'])) #str
# stopoverPeriod = i["productInfoList"][0]["stopoverPeriod"] #3
# stopoverMinute = i["productInfoList"][0]["stopoverMinute"] #int 960
# flightInfoList = i["productInfoList"][0]["flightInfoList"]
# if i["productInfoList"][0]['policyInfoList'][0]['priceDetailInfo']['adult'] != None:
#     flightPriceAdult = i["productInfoList"][0]['policyInfoList'][0]['priceDetailInfo']['adult']['totalPrice'] #int
#     print(flightPriceAdult)
# if i["productInfoList"][0]['policyInfoList'][0]['priceDetailInfo']['child'] != None:
#     flightPriceChild = i["productInfoList"][0]['policyInfoList'][0]['priceDetailInfo']['child']['totalPrice'] #int
#     print(flightPriceChild)
# totalPrice = i["productInfoList"][0]['policyInfoList'][0]['priceDetailInfo']['viewTotalPrice']
# for item in flightInfoList:
#     f1atime = item['aDateTime']#str
#     f1dcity = item['dCityInfo']['name']+" "+item['dPortInfo']['code']+" "+item['dPortInfo']['name']+" "+item['dPortInfo']['terminal'] #台北 TPE 桃園機場
#     f1acity = item['aCityInfo']['name']+" "+item['aPortInfo']['code']+" "+item['aPortInfo']['name']+" "+item['aPortInfo']['terminal'] #台北 TPE 桃園機場
#     f1planecor = item['airlineInfo']['name']+" "+item['flightNo'] #真航空 LJ211
#     f1plane = item['craftInfo']['name']+" "+i["productInfoList"][0]['policyInfoList'][0]['productClass'][0] #波音737-800 經濟艙
#     stayoverNum = str(i["productInfoList"][0]["filterInfoList"][0]['stopType'])+"個中轉站"# 1個中轉站 str
#     stayoverAirport = item['dPortInfo']['code']+'-'+stayoverNum+'-'+item['aPortInfo']['code']# ICN-1個中轉站-KIX str
#     airplaneCompany = item['airlineInfo']['name'] #真 航空
#     print(f1atime)
#     print(f1dcity)
#     print(f1acity)
#     print(f1planecor)
#     print(f1plane)
#     print(stayoverNum)
#     print(stayoverAirport)
#     print(airplaneCompany)
# duratime = str(durationHour)+"小時"+str(durationMin)+"分鐘"
# print(duratime,dDateTime,aDateTime, stopoverPeriod,stopoverMinute)
# print(avbTickets)
# print(filterInfoListdtime)
# print(filterInfoListatime)
# print(totalPrice)