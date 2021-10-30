import re
import requests
import json,random
from pymongo import MongoClient
import concurrent.futures
from env import config
import requests
import json
from datetime import date
import pymysql


def api_create_hotel():
    rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
                            user="admin",password=config.RDSMASTERPASSWORD,\
                            port=3306,database="skike",\
                            cursorclass = pymysql.cursors.DictCursor)
    cursor = rdsDB.cursor()
    conn = MongoClient("mongodb://localhost:{}/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false".format(config.MONGO_PASS_SKIKE_LOCAL))
    mydatabase = conn['skike'] 
    # Access collection of the database 
    mycollection=mydatabase['(2021-10-25)skike_hotel_v2']
    pipetest = [
    {
        '$project': {
            'priceHistogram': 0, 
            'topConcepts.center.nsid': 0, 
            'uiv': 0, 
            'userBookingIntent': 0, 
            'pollData': 0, 
            'clcklBase': 0, 
            '__typename': 0
        }
    }, {
        '$limit': 20
    }
]
    result =mycollection.aggregate(pipetest)
    results = [doc for doc in result]
    for i in results[0:1]:
        data_list = []
        for hotel_product in i['accommodations']:
            hotel_id = hotel_product['id']['id']
            data_query_time = i['dataQueryTime']
            hotel_name = hotel_product['name']['value']
            hotel_category = hotel_product['accommodationType']['value']
            hotel_location =  hotel_product['locality']['value']
            hotel_image = hotel_product['images']['mainUri']
            hotel_geo_lat = hotel_product['geocode']['lat']
            hotel_geo_lng = hotel_product['geocode']['lng']
            data_list.append((hotel_id,data_query_time,hotel_name,hotel_category,hotel_location,hotel_image,hotel_geo_lat,hotel_geo_lng))
            category_list = ['bestPrice','alternative']
            agency_data_list =[]
            # for category in category_list:
            #     #best agency
            #     if category == "bestPrice":
            #         hotel_alternative_agency = hotel_product['deals'][category]['name']['value']
            #         print('bestPrice')
            #         agency_logo = hotel_product['deals'][category]['advertiserLogo']['url']
            #         hotel_feature =""
            #         for data in hotel_product['deals'][category]['priceAttributes']:
            #             try:
            #                 hotel_feature+=data['name']['value']+', '
            #             except Exception as e:
            #                 print("Exeception occured:{}".format(e))
            #         hotel_price = hotel_product['deals'][category]['price']
            #         hotel_url =""
            #         agency_data_list.append((hotel_alternative_agency,agency_logo,hotel_feature,hotel_price,hotel_url,hotel_id))
            #         print('bestPriceappend')
            #     #alternative agency
            #     elif category == "alternative":
            #         for alternative_item in hotel_product['deals'][category]:
            #             hotel_alternative_agency = alternative_item['name']['value']
            #             # agency_logo = alternative_item['advertiserLogo']['url']
            #             hotel_feature =""
            #             for data in alternative_item['priceAttributes']:
            #                 try:
            #                     hotel_feature+=data['name']['value']+', '
            #                 except Exception as e:
            #                     print("Exeception occured:{}".format(e))
            #             print(hotel_feature)
            #             hotel_price = alternative_item['price']
            #             hotel_url =""
            #             agency_data_list.append((hotel_alternative_agency,agency_logo,hotel_feature,hotel_price,hotel_url,hotel_id))
            #     print(category)
            #     sql_agency = "INSERT INTO skike.hotel_alternative ( `hotel_agency`, `agency_logo`, `hotel_feature`, `price`, `hotel_url`, `hotel_id`)VALUES (%s, %s, %s, %s, %s, %s)"

            # try:
            #     cursor.executemany(sql_agency,agency_data_list)
            #     rdsDB.commit()
            # except Exception as e:
            #     print("Exeception occured:{}".format(e))

        sql_hotel = "INSERT INTO skike.hotel (`id`, `data_query_time`, `name`, `category`, `locality`, `image_url`, `geocode_lat`, `geocode_lng`)VALUES (%s, %s, %s, %s, %s, %s,%s,%s)"
        try:
            cursor.executemany(sql_hotel,data_list)
            rdsDB.commit()
        except Exception as e:
            print("Exeception occured:{}".format(e))

        
        sql = "SELECT id FROM skike.hotel"
        cursor.execute(sql)
        sql_all_hotel_id = cursor.fetchall()
    return sql_all_hotel_id


def get_hotel_price_list(list):
  with open('Webshare 10 proxies.txt') as f:
      # data = json.load(f)
      data = f.read()
      m=re.findall('\d+\.\d+\.\d+\.\d+:\d+',data)
      f.close()
      print(m)

  url = "https://www.trivago.com.tw/graphql"
  for hotel_id in list:
    payload = json.dumps({
      "operationName": "getAccommodationDeals",
      "variables": {
        "accommodationDealsParams": {
          "accommodationNsid": {
            "id": hotel_id,
            "ns": 100
          },
          "stayPeriod": {
            "arrival": "2021-11-04",
            "departure": "2021-11-05"
          },
          "rooms": [
            {
              "adults": 1,
              "children": []
            }
          ],
          "tid": "0882dd417534e3d783b2d8155d",
          "platform": "tw",
          "currency": "TWD",
          "language": "zh-Hant-TW",
          "clientSideDecorated": 1,
          "clientApplicationType": 1,
          "priceTypeRestrictions": [
            1
          ],
          "parentRequestId": "1d8b804f-c77f-4876-bccb-a40e6f43a280",
          "channel": {
            "branded": {
              "isStandardDate": False,
              "stayPeriodSource": {
                "value": 22
              }
            }
          },
          "deviceType": "DESKTOP_CHROME"
        },
        "advertiserLogoUrlParams": {
          "locale": "TW"
        },
        "pollData": None
      },
      "extensions": {
        "persistedQuery": {
          "version": 1,
          "sha256Hash": "3ec743eef81a9d65eb8a4fdaa0b0018954c00fce980834cff1e09bc0f66379bf"
        }
      }
    })
    headers = {
      'cookie': 'PHPSESSID=f491b4e0ed1583e865b01bb1c4037eb1; trv_tid=0882dd417534e3d783b2d8155d; sLanguageLocale=TW; tid=0882dd417534e3d783b2d8155d; GROUP=nsi; edge_tid_s=0882dd417534e3d783b2d8155d; edge_tid=0882dd417534e3d783b2d8155d; iDisableRedirect=1; trv_cal_int=true; ak_bmsc=653EB15AEAAB7DB60F7BB1174134A96D~000000000000000000000000000000~YAAQBtfSFwhi/Vd8AQAAIISMlg1Ibfjik4xi+0Y7F4YBXL0RM/Sx5WDM8PPi5RGaxExCkT27bX/VPt6pXlykbyuUKgSc7szSf1/AAsNtA5EGVTdurBzDkAh4sV8vTk4U2QjsMq+zemJ6lK27JOc2kE1bHNbG/oAoVF4P3Lc6KHfmMEfEq3LrRRLwh6NVNytEELWkhoQ+g08LPiFvqLCeeDEutqa7cv/xZLbtDFWkwuLFXiUAUKrRJrcLlU6Z676qg0SbQRXv1hE9oeRJP4V2diHmjlzb0CbrDGx88oX+cmfWjCokeyyyayl8/BPivfuZRGQ0hcWsTlpeRXgBppS3E+phKzgRFqzC7Bp0yu1ZfYyfUKh9QiAZIi6eh7Tqz1/uCsyjBXU9OJDTogsZD0JGTZw2b1JEoqbJkT7SC+5xZFOxMwZfkqg0o86E/a/EziYJS2xVkeCDLFVV/vCCOzW6D7CKu2S/L7uhbPb5XYxDlshH/mSkS1tzGVk/y6Qy; _gcl_au=1.1.238118696.1634613364; g_state={"i_p":1634620567480,"i_l":1}; reseor=71692/200%2C194/200; sCurrentPlatformLocale=TW; ftv=%7B%22ftv%22%3A%2220211019031602%22%2C%22ltv%22%3A%2220211019031602%22%2C%22ep%22%3A9999%2C%22cntv%22%3A1%2C%22cntc%22%3A0%2C%22cntcs%22%3A0%2C%22fep%22%3A9999%2C%22vc%22%3A0%2C%22ctl%22%3A106%2C%22ctf%22%3A106%2C%22item%22%3A0%2C%22path%22%3A91534%2C%22path2%22%3A91534%7D; trv_dt_src={%22dateSource%22:22%2C%22dateRange%22:{%22arrival%22:{%22day%22:24%2C%22month%22:10%2C%22year%22:2021}%2C%22departure%22:{%22day%22:25%2C%22month%22:10%2C%22year%22:2021}}}; _yoid=89ca3b15-5c81-423c-814b-c3b546dcda49; _yosid=fc5c4b0a-2db3-42c9-986e-04e3f2053250; attrChannel=seo; sessionDuration=30000; gtmClickCount=true; RT="z=1&dm=www.trivago.com.tw&si=e23ea991-149d-40ab-a372-075e731d6017&ss=kuxil9db&sl=3&tt=44i&bcn=%2F%2F684d0d3e.akstat.io%2F"; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Oct+19+2021+11%3A31%3A41+GMT%2B0800+(%E5%8F%B0%E5%8C%97%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=6.20.0&isIABGlobal=false&hosts=&consentId=0c737b02-e9a0-4211-a8f2-d5ba02e29d69&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1&geolocation=TW%3BTPE&AwaitingReconsent=false; OptanonAlertBoxClosed=2021-10-19T03:31:41.236Z; firstpage=false; pageviewCount=2; _uetsid=e769eac0308a11ecae6fbbeb32a0526f; _uetvid=e76a3910308a11ecb88381ad56ce4ed5; edge_tid=0882dd417534e3d783b2d8155d; edge_tid_s=0882dd417534e3d783b2d8155d',
      'referer': 'https://www.trivago.com.tw/?aDateRange[arr]=2021-10-24&aDateRange[dep]=2021-10-25&aPriceRange[from]=0&aPriceRange[to]=0&iRoomType=7&aRooms[0][adults]=2&cpt2=71692/200&hasList=1&hasMap=0&bIsSeoPage=0&sortingId=1&slideoutsPageItemId=&iGeoDistanceLimit=20000&address=&addressGeoCode=&offset=0&ra=&overlayMode=',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
      'authority': 'www.trivago.com.tw',
      'method': 'POST',
      'path': '/graphql',
      'scheme': 'https',
      'content-type': 'application/json',
      'origin': 'https://www.trivago.com.tw',
      'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'x-trv-app-id': 'HS_WEB_APP',
      'x-trv-cst': '32046,38217,45104,45749,45766,46136,46164,46535,47828,47908,48405,48506,48508,48542,48681,49291,49382,49419,49696,49752,49777,50553,50567,50805,50950,51032,51076,51246,51458,51591,51619,51886,51913,52217,52219,52345,52366,52551,52590,52756,52830,52891,52949,53005,53018,53183,53192,53231,53393,53508,53513,53593,53687,53852,53894,54061,54244,54273,54333,54362,54596,54827,54858,54889,54999,55003,55113,55133,55134,55136,55145,55353,55451,55628,55690,55739,55866,56275-3,56467-1,56477,56578,56633,56861-3,56937-2,57155,57488,57889-2,58038,58205,58324-1,58328-1,58387,58433',
      'x-trv-language': 'zh-Hant-TW',
      'x-trv-platform': 'tw',
      'x-trv-tid': '0882dd417534e3d783b2d8155d',
      'accept': '*/*',
      'accept-encoding': 'gzip, deflate, br',
      'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
      'apollographql-client-name': 'hs-web',
      'apollographql-client-version': 'v93_10_5_ae_f07e1e495a0'
    }

    conn = MongoClient("mongodb://localhost:{}/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false".format(config.MONGO_PASS_SKIKE_LOCAL))
    mydatabase = conn['skike'] 
    # Access collection of the database 
    mycollection=mydatabase['({})hotel_detail_skike'.format(str(date.today()))]

    ip = random.choice(m)
    proxies = {'http':"http://{}:{}@{}".format('vvbocpqj','obt7b7ug0dim',ip)}
    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
    result = response.json()
    mycollection.insert_one(result)

get_hotel_price_list(api_create_hotel())