import requests
from env import config
import time,json
from datetime import timedelta
import polyline

# print(str(int(time.time())))

url = "https://maps.googleapis.com/maps/api/directions/json?language=zh-TW&origin=37.559,126.794&destination=37.6077,127.078&mode=transit&key={}".format(config.GOOGLE_API_KEY)
#thiswork
# url = "https://maps.googleapis.com/maps/api/directions/json?origin=41.9027835,12.496365500000024&destination=45.4642035,9.189981999999986&mode=transit&key={}".format(config.GOOGLE_API_KEY)
#this original
# url = "https://maps.googleapis.com/maps/api/directions/json?language=zh-TW&origin=東京國際機場&destination=東京大學&mode=transit&departure_time={}&key={}".format(str(int(time.time())+200),config.GOOGLE_API_KEY)
# b = int(time.time())
# a = int(time.time())+200
# print( b,a)
# print(str(int(time.time())))
payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

# with open(r"C:\Users\Ben Fan\Desktop\skike\Main_20211013_project\testmap.json",encoding="utf-8") as f:
#     i= json.load(f)
#     for item in i['routes'][0:1]:
#         for item2 in item['legs'][0:1]:
#             for item3 in item2['steps']:
#                 print(item3)
#                 print("---------------------------------------")
#                 print(polyline.decode(item3['polyline']['points']))
