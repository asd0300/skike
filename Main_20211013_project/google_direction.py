import requests
from env import config
import time,json
import polyline

# print(str(int(time.time())))
# url = "https://maps.googleapis.com/maps/api/directions/json?language=zh-TW&origin=Hsinchu&destination=Taipei&mode=transit&departure_time={}&key={}".format(str(int(time.time())),config.GOOGLE_API_KEY)

# payload={}
# headers = {}

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)

with open(r"C:\Users\Ben Fan\Desktop\skike\Main_20211013_project\testmap.json",encoding="utf-8") as f:
    i= json.load(f)
    for item in i['routes'][0:1]:
        for item2 in item['legs'][0:1]:
            for item3 in item2['steps']:
                print(item3)
                print("---------------------------------------")
                print(polyline.decode(item3['polyline']['points']))
