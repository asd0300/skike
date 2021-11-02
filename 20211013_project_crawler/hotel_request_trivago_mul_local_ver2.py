import time,re
import requests
import json,random
from env import param
from pymongo import MongoClient
import concurrent.futures
from env import config

###date generator
from datetime import date, timedelta

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
####

conn = MongoClient("mongodb://localhost:{}/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false".format(config.MONGO_PASS_SKIKE_LOCAL))
mydatabase = conn['skike'] 
# Access collection of the database 
mycollection=mydatabase['({})skike_hotel_v2'.format(str(date.today()))]

with open('Webshare 10 proxies.txt') as f:
    # data = json.load(f)
    data = f.read()
    m=re.findall('\d+\.\d+\.\d+\.\d+:\d+',data)
    f.close()
    print(m)


def gettotal(locLN1,locLN2,dateTodate,count=0):
    url = "https://www.trivago.com.tw/graphql"
    param = '''{{"dt":1,"iph":1,"tz":-480,"pra":"","channel":"b,isd:0,sps:22","csid":8,"ccid":"YX9CFzSWmdCkW77jr9ytmQAAAAA","adl":3,"crcl":"{},20000","s":"0","uiv":"{}/200:1","tid":"0882dd417534e3d783b2d8155d","sp":"{}","rms":"1","p":"tw","l":"zh-Hant-TW","ccy":"TWD","accoff":{},"acclim":25}}'''.format(locLN1,locLN2,dateTodate,count)
    # print(1)
    # print(param)
    param.replace('"','\"')

    payload = json.dumps({
    "operationName": "regionSearch",
    "variables": {
        "searchType": "cep.json",
        "queryParams": param.replace('"','\"'),
        "minEurocentPrice": 5226,
        "maxEurocentPrice": 52262,
        "pollData": None,
        "bucketIntervals": [
        [
            5226,
            5598
        ],
        [
            5599,
            5999
        ],
        [
            6000,
            6578
        ],
        [
            6579,
            7048
        ],
        [
            7049,
            7552
        ],
        [
            7553,
            8281
        ],
        [
            8282,
            8874
        ],
        [
            8875,
            9508
        ],
        [
            9509,
            10189
        ],
        [
            10190,
            11172
        ],
        [
            11173,
            11971
        ],
        [
            11972,
            13126
        ],
        [
            13127,
            14065
        ],
        [
            14066,
            15071
        ],
        [
            15072,
            16525
        ],
        [
            16526,
            17707
        ],
        [
            17708,
            18973
        ],
        [
            18974,
            20804
        ],
        [
            20805,
            22292
        ],
        [
            22293,
            23887
        ],
        [
            23888,
            26191
        ],
        [
            26192,
            28065
        ],
        [
            28066,
            30072
        ],
        [
            30073,
            32973
        ],
        [
            32974,
            35332
        ],
        [
            35333,
            37859
        ],
        [
            37860,
            40567
        ],
        [
            40568,
            44481
        ],
        [
            44482,
            52262
        ],
        [
            52263,
            2147483647
        ]
        ],
        "isSponsoredListings": True,
      "advertiserLogoUrlParams": {
        "locale": "TW",
        "width": 68
      },
      "openItemsInNewTab": False,
      "showBudgetHotels": True,
      "isMobileList": False,
      "shouldSkipRedirect": True,
      "aaScoreRating": False,
      "houseApartmentType": True,
      "locale": "TW",
      "cidns": "71462/200",
      "isVRBOOLB": True,
      "allowTrivagoPriceIndex": False,
      "showExclusiveBookingRatings": True,
      "getExclusiveVRBORatings": True,
      "amenities": False,
      "isWARPForwarder": False,
      "getFlashDeals": True,
      "shouldShowNewSpecialOffers": True
    },
    "extensions": {
        "persistedQuery": {
        "version": 1,
        "sha256Hash": "7c98fbb21b5e29f6224ebd9ca383c2b9512e6e8d27e8b936a3a4ff502c1b2037"
        }
    }
    })
    headers = {
    'cookie': 'PHPSESSID=f491b4e0ed1583e865b01bb1c4037eb1; trv_tid=0882dd417534e3d783b2d8155d; sLanguageLocale=TW; tid=0882dd417534e3d783b2d8155d; GROUP=nsi; edge_tid_s=0882dd417534e3d783b2d8155d; edge_tid=0882dd417534e3d783b2d8155d; iDisableRedirect=1; trv_cal_int=true; ak_bmsc=653EB15AEAAB7DB60F7BB1174134A96D~000000000000000000000000000000~YAAQBtfSFwhi/Vd8AQAAIISMlg1Ibfjik4xi+0Y7F4YBXL0RM/Sx5WDM8PPi5RGaxExCkT27bX/VPt6pXlykbyuUKgSc7szSf1/AAsNtA5EGVTdurBzDkAh4sV8vTk4U2QjsMq+zemJ6lK27JOc2kE1bHNbG/oAoVF4P3Lc6KHfmMEfEq3LrRRLwh6NVNytEELWkhoQ+g08LPiFvqLCeeDEutqa7cv/xZLbtDFWkwuLFXiUAUKrRJrcLlU6Z676qg0SbQRXv1hE9oeRJP4V2diHmjlzb0CbrDGx88oX+cmfWjCokeyyyayl8/BPivfuZRGQ0hcWsTlpeRXgBppS3E+phKzgRFqzC7Bp0yu1ZfYyfUKh9QiAZIi6eh7Tqz1/uCsyjBXU9OJDTogsZD0JGTZw2b1JEoqbJkT7SC+5xZFOxMwZfkqg0o86E/a/EziYJS2xVkeCDLFVV/vCCOzW6D7CKu2S/L7uhbPb5XYxDlshH/mSkS1tzGVk/y6Qy; _gcl_au=1.1.238118696.1634613364; g_state={"i_p":1634620567480,"i_l":1}; reseor=71692/200%2C194/200; sCurrentPlatformLocale=TW; ftv=%7B%22ftv%22%3A%2220211019031602%22%2C%22ltv%22%3A%2220211019031602%22%2C%22ep%22%3A9999%2C%22cntv%22%3A1%2C%22cntc%22%3A0%2C%22cntcs%22%3A0%2C%22fep%22%3A9999%2C%22vc%22%3A0%2C%22ctl%22%3A106%2C%22ctf%22%3A106%2C%22item%22%3A0%2C%22path%22%3A91534%2C%22path2%22%3A91534%7D; trv_dt_src={%22dateSource%22:22%2C%22dateRange%22:{%22arrival%22:{%22day%22:24%2C%22month%22:10%2C%22year%22:2021}%2C%22departure%22:{%22day%22:25%2C%22month%22:10%2C%22year%22:2021}}}; _yoid=89ca3b15-5c81-423c-814b-c3b546dcda49; _yosid=fc5c4b0a-2db3-42c9-986e-04e3f2053250; attrChannel=seo; sessionDuration=30000; gtmClickCount=true; RT="z=1&dm=www.trivago.com.tw&si=e23ea991-149d-40ab-a372-075e731d6017&ss=kuxil9db&sl=3&tt=44i&bcn=%2F%2F684d0d3e.akstat.io%2F"; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Oct+19+2021+11%3A31%3A41+GMT%2B0800+(%E5%8F%B0%E5%8C%97%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=6.20.0&isIABGlobal=false&hosts=&consentId=0c737b02-e9a0-4211-a8f2-d5ba02e29d69&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1&geolocation=TW%3BTPE&AwaitingReconsent=false; OptanonAlertBoxClosed=2021-10-19T03:31:41.236Z; firstpage=false; pageviewCount=2; _uetsid=e769eac0308a11ecae6fbbeb32a0526f; _uetvid=e76a3910308a11ecb88381ad56ce4ed5; edge_tid=0882dd417534e3d783b2d8155d; edge_tid_s=0882dd417534e3d783b2d8155d',
    'referer': 'https://www.trivago.com.tw/?aDateRange[arr]=2021-10-24&aDateRange[dep]=2021-10-25&aPriceRange[from]=0&aPriceRange[to]=0&iRoomType=7&aRooms[0][adults]=2&cpt2=71692/200&hasList=1&hasMap=0&bIsSeoPage=0&sortingId=1&slideoutsPageItemId=&iGeoDistanceLimit=20000&address=&addressGeoCode=&offset=0&ra=&overlayMode=',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
    'authority': 'www.trivago.com.tw',
    'method': 'POST',
    'path': '/graphql',
    'scheme': 'https',
    'content-type': 'application/json',
    'origin': 'https://www.trivago.com.tw',
    'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'x-trv-app-id': 'HS_WEB_APP',
    'x-trv-cst': '32046,38217,45104,45749,45766,46136,46164,46535,47828,47908,48405,48506,48508,48542,48681,49291,49382,49419,49696,49752,49777,50553,50567,50805,50950,51032,51076,51246,51458,51591,51619,51886,51913,52217,52219,52345,52366,52551,52590,52756,52830,52891,52949,53005,53018,53183,53192,53231,53393,53508,53513,53593,53687,53852,53894,54061,54244,54273,54333,54362,54596,54827,54858,54889,54999,55003,55113,55133,55134,55136,55145,55353,55451,55628,55690,55739,55866,56275-3,56467-1,56477,56578,56633,56861-3,56937-2,57155,57488,57889-2,58038,58131,58205,58433',
    'x-trv-language': 'zh-Hant-TW',
    'x-trv-platform': 'tw',
    'x-trv-tid': '0882dd417534e3d783b2d8155d',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'apollographql-client-name': 'hs-web',
    'apollographql-client-version': 'v93_10_5_ae_f07e1e495a0'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    result = response.json()['data']['rs']['totalCount']
    return result

def getHotelNoSave(locLN1,locLN2,dateTodate,count=0):
    try:
        url = "https://www.trivago.com.tw/graphql"
        # param = '''{{"dt":1,"iph":1,"tz":-480,"pra":"","channel":"seo,isd:0,sps:22","csid":8,"ccid":"YW5pqN3e6sg8Jp1PzORUdgAAABY","adl":3,"crcl":"{},20000","s":"0","uiv":"{}/200:1","tid":"0882dd417534e3d783b2d8155d","sp":"{}","rms":"2","p":"tw","l":"zh-Hant-TW","ccy":"TWD","accoff":{},"acclim":25}}'''.format(locLN1,locLN2,dateTodate,count)
        param = '''{{"dt":1,"iph":1,"tz":-480,"pra":"","channel":"b,isd:0,sps:22","csid":8,"ccid":"YX9CFzSWmdCkW77jr9ytmQAAAAA","adl":3,"crcl":"{},20000","s":"0","uiv":"{}/200:1","tid":"0882dd417534e3d783b2d8155d","sp":"{}","rms":"1","p":"tw","l":"zh-Hant-TW","ccy":"TWD","accoff":{},"acclim":25}}'''.format(locLN1,locLN2,dateTodate,count)
        # print(1)
        # print(param)
        param.replace('"','\"')

        payload = json.dumps({
        "operationName": "regionSearch",
        "variables": {
            "searchType": "cep.json",
            "queryParams": param.replace('"','\"'),
            "minEurocentPrice": 5226,
            "maxEurocentPrice": 52262,
            "pollData": None,
            "bucketIntervals": [
            [
                5226,
                5598
            ],
            [
                5599,
                5999
            ],
            [
                6000,
                6578
            ],
            [
                6579,
                7048
            ],
            [
                7049,
                7552
            ],
            [
                7553,
                8281
            ],
            [
                8282,
                8874
            ],
            [
                8875,
                9508
            ],
            [
                9509,
                10189
            ],
            [
                10190,
                11172
            ],
            [
                11173,
                11971
            ],
            [
                11972,
                13126
            ],
            [
                13127,
                14065
            ],
            [
                14066,
                15071
            ],
            [
                15072,
                16525
            ],
            [
                16526,
                17707
            ],
            [
                17708,
                18973
            ],
            [
                18974,
                20804
            ],
            [
                20805,
                22292
            ],
            [
                22293,
                23887
            ],
            [
                23888,
                26191
            ],
            [
                26192,
                28065
            ],
            [
                28066,
                30072
            ],
            [
                30073,
                32973
            ],
            [
                32974,
                35332
            ],
            [
                35333,
                37859
            ],
            [
                37860,
                40567
            ],
            [
                40568,
                44481
            ],
            [
                44482,
                52262
            ],
            [
                52263,
                2147483647
            ]
            ],
            "isSponsoredListings": True,
            "advertiserLogoUrlParams": {
                "locale": "TW",
                "width": 68
            },
            "openItemsInNewTab": False,
            "showBudgetHotels": True,
            "isMobileList": False,
            "shouldSkipRedirect": True,
            "aaScoreRating": False,
            "houseApartmentType": True,
            "locale": "TW",
            "cidns": "71462/200",
            "isVRBOOLB": True,
            "allowTrivagoPriceIndex": False,
            "showExclusiveBookingRatings": True,
            "getExclusiveVRBORatings": True,
            "amenities": False,
            "isWARPForwarder": False,
            "getFlashDeals": True,
            "shouldShowNewSpecialOffers": True
        },
        "extensions": {
            "persistedQuery": {
            "version": 1,
            "sha256Hash": "7c98fbb21b5e29f6224ebd9ca383c2b9512e6e8d27e8b936a3a4ff502c1b2037"
            }
        }
        })
        headers = {
        'cookie': 'PHPSESSID=f491b4e0ed1583e865b01bb1c4037eb1; trv_tid=0882dd417534e3d783b2d8155d; sLanguageLocale=TW; tid=0882dd417534e3d783b2d8155d; GROUP=nsi; edge_tid_s=0882dd417534e3d783b2d8155d; edge_tid=0882dd417534e3d783b2d8155d; iDisableRedirect=1; trv_cal_int=true; ak_bmsc=653EB15AEAAB7DB60F7BB1174134A96D~000000000000000000000000000000~YAAQBtfSFwhi/Vd8AQAAIISMlg1Ibfjik4xi+0Y7F4YBXL0RM/Sx5WDM8PPi5RGaxExCkT27bX/VPt6pXlykbyuUKgSc7szSf1/AAsNtA5EGVTdurBzDkAh4sV8vTk4U2QjsMq+zemJ6lK27JOc2kE1bHNbG/oAoVF4P3Lc6KHfmMEfEq3LrRRLwh6NVNytEELWkhoQ+g08LPiFvqLCeeDEutqa7cv/xZLbtDFWkwuLFXiUAUKrRJrcLlU6Z676qg0SbQRXv1hE9oeRJP4V2diHmjlzb0CbrDGx88oX+cmfWjCokeyyyayl8/BPivfuZRGQ0hcWsTlpeRXgBppS3E+phKzgRFqzC7Bp0yu1ZfYyfUKh9QiAZIi6eh7Tqz1/uCsyjBXU9OJDTogsZD0JGTZw2b1JEoqbJkT7SC+5xZFOxMwZfkqg0o86E/a/EziYJS2xVkeCDLFVV/vCCOzW6D7CKu2S/L7uhbPb5XYxDlshH/mSkS1tzGVk/y6Qy; _gcl_au=1.1.238118696.1634613364; g_state={"i_p":1634620567480,"i_l":1}; reseor=71692/200%2C194/200; sCurrentPlatformLocale=TW; ftv=%7B%22ftv%22%3A%2220211019031602%22%2C%22ltv%22%3A%2220211019031602%22%2C%22ep%22%3A9999%2C%22cntv%22%3A1%2C%22cntc%22%3A0%2C%22cntcs%22%3A0%2C%22fep%22%3A9999%2C%22vc%22%3A0%2C%22ctl%22%3A106%2C%22ctf%22%3A106%2C%22item%22%3A0%2C%22path%22%3A91534%2C%22path2%22%3A91534%7D; trv_dt_src={%22dateSource%22:22%2C%22dateRange%22:{%22arrival%22:{%22day%22:24%2C%22month%22:10%2C%22year%22:2021}%2C%22departure%22:{%22day%22:25%2C%22month%22:10%2C%22year%22:2021}}}; _yoid=89ca3b15-5c81-423c-814b-c3b546dcda49; _yosid=fc5c4b0a-2db3-42c9-986e-04e3f2053250; attrChannel=seo; sessionDuration=30000; gtmClickCount=true; RT="z=1&dm=www.trivago.com.tw&si=e23ea991-149d-40ab-a372-075e731d6017&ss=kuxil9db&sl=3&tt=44i&bcn=%2F%2F684d0d3e.akstat.io%2F"; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Oct+19+2021+11%3A31%3A41+GMT%2B0800+(%E5%8F%B0%E5%8C%97%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=6.20.0&isIABGlobal=false&hosts=&consentId=0c737b02-e9a0-4211-a8f2-d5ba02e29d69&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1&geolocation=TW%3BTPE&AwaitingReconsent=false; OptanonAlertBoxClosed=2021-10-19T03:31:41.236Z; firstpage=false; pageviewCount=2; _uetsid=e769eac0308a11ecae6fbbeb32a0526f; _uetvid=e76a3910308a11ecb88381ad56ce4ed5; edge_tid=0882dd417534e3d783b2d8155d; edge_tid_s=0882dd417534e3d783b2d8155d',
        'referer': 'https://www.trivago.com.tw/?aDateRange[arr]=2021-10-24&aDateRange[dep]=2021-10-25&aPriceRange[from]=0&aPriceRange[to]=0&iRoomType=7&aRooms[0][adults]=2&cpt2=71692/200&hasList=1&hasMap=0&bIsSeoPage=0&sortingId=1&slideoutsPageItemId=&iGeoDistanceLimit=20000&address=&addressGeoCode=&offset=0&ra=&overlayMode=',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        'authority': 'www.trivago.com.tw',
        'method': 'POST',
        'path': '/graphql',
        'scheme': 'https',
        'content-type': 'application/json',
        'origin': 'https://www.trivago.com.tw',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'x-trv-app-id': 'HS_WEB_APP',
        'x-trv-cst': '32046,38217,45104,45749,45766,46136,46164,46535,47828,47908,48405,48506,48508,48542,48681,49291,49382,49419,49696,49752,49777,50553,50567,50805,50950,51032,51076,51246,51458,51591,51619,51886,51913,52217,52219,52345,52366,52551,52590,52756,52830,52891,52949,53005,53018,53183,53192,53231,53393,53508,53513,53593,53687,53852,53894,54061,54244,54273,54333,54362,54596,54827,54858,54889,54999,55003,55113,55133,55134,55136,55145,55353,55451,55628,55690,55739,55866,56275-3,56467-1,56477,56578,56633,56861-3,56937-2,57155,57488,57889-2,58038,58131,58205,58433',
        'x-trv-language': 'zh-Hant-TW',
        'x-trv-platform': 'tw',
        'x-trv-tid': '0882dd417534e3d783b2d8155d',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'apollographql-client-name': 'hs-web',
        'apollographql-client-version': 'v93_10_5_ae_f07e1e495a0'
        }
        ip = random.choice(m)
        proxies = {'http':"http://{}:{}@{}".format('vvbocpqj','obt7b7ug0dim',ip)}
        response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
        result = response.json()
        resulthotel = result['data']['rs']
        count+=25
        print(str(count)+" "+str(dateTodate)+" ip is "+str(ip)+" No save")
        # mycollection.insert_one(resulthotel)
    except Exception as e:
        print("ERROR:", url, e)

def getHotel(locLN1,locLN2,dateTodate,count=0):
    total = gettotal(locLN1,locLN2,dateTodate,count=0)
    # total =51
    while (total>count):
        try:
            url = "https://www.trivago.com.tw/graphql"
            param = '''{{"dt":1,"iph":1,"tz":-480,"pra":"","channel":"b,isd:0,sps:22","csid":8,"ccid":"YX9CFzSWmdCkW77jr9ytmQAAAAA","adl":3,"crcl":"{},20000","s":"0","uiv":"{}/200:1","tid":"0882dd417534e3d783b2d8155d","sp":"{}","rms":"1","p":"tw","l":"zh-Hant-TW","ccy":"TWD","accoff":{},"acclim":25}}'''.format(locLN1,locLN2,dateTodate,count)
            # print(1)
            # print(param)
            param.replace('"','\"')

            payload = json.dumps({
            "operationName": "regionSearch",
            "variables": {
                "searchType": "cep.json",
                "queryParams": param.replace('"','\"'),
                "minEurocentPrice": 5226,
                "maxEurocentPrice": 52262,
                "pollData": None,
                "bucketIntervals": [
                [
                    5226,
                    5598
                ],
                [
                    5599,
                    5999
                ],
                [
                    6000,
                    6578
                ],
                [
                    6579,
                    7048
                ],
                [
                    7049,
                    7552
                ],
                [
                    7553,
                    8281
                ],
                [
                    8282,
                    8874
                ],
                [
                    8875,
                    9508
                ],
                [
                    9509,
                    10189
                ],
                [
                    10190,
                    11172
                ],
                [
                    11173,
                    11971
                ],
                [
                    11972,
                    13126
                ],
                [
                    13127,
                    14065
                ],
                [
                    14066,
                    15071
                ],
                [
                    15072,
                    16525
                ],
                [
                    16526,
                    17707
                ],
                [
                    17708,
                    18973
                ],
                [
                    18974,
                    20804
                ],
                [
                    20805,
                    22292
                ],
                [
                    22293,
                    23887
                ],
                [
                    23888,
                    26191
                ],
                [
                    26192,
                    28065
                ],
                [
                    28066,
                    30072
                ],
                [
                    30073,
                    32973
                ],
                [
                    32974,
                    35332
                ],
                [
                    35333,
                    37859
                ],
                [
                    37860,
                    40567
                ],
                [
                    40568,
                    44481
                ],
                [
                    44482,
                    52262
                ],
                [
                    52263,
                    2147483647
                ]
                ],
                "isSponsoredListings": True,
                "advertiserLogoUrlParams": {
                    "locale": "TW",
                    "width": 68
                },
                "openItemsInNewTab": False,
                "showBudgetHotels": True,
                "isMobileList": False,
                "shouldSkipRedirect": True,
                "aaScoreRating": False,
                "houseApartmentType": True,
                "locale": "TW",
                "cidns": "71462/200",
                "isVRBOOLB": True,
                "allowTrivagoPriceIndex": False,
                "showExclusiveBookingRatings": True,
                "getExclusiveVRBORatings": True,
                "amenities": False,
                "isWARPForwarder": False,
                "getFlashDeals": True,
                "shouldShowNewSpecialOffers": True
                },
                "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "7c98fbb21b5e29f6224ebd9ca383c2b9512e6e8d27e8b936a3a4ff502c1b2037"
                }
                }
            })
            headers = {
            'cookie': 'PHPSESSID=f491b4e0ed1583e865b01bb1c4037eb1; trv_tid=0882dd417534e3d783b2d8155d; sLanguageLocale=TW; tid=0882dd417534e3d783b2d8155d; GROUP=nsi; edge_tid_s=0882dd417534e3d783b2d8155d; edge_tid=0882dd417534e3d783b2d8155d; iDisableRedirect=1; trv_cal_int=true; ak_bmsc=653EB15AEAAB7DB60F7BB1174134A96D~000000000000000000000000000000~YAAQBtfSFwhi/Vd8AQAAIISMlg1Ibfjik4xi+0Y7F4YBXL0RM/Sx5WDM8PPi5RGaxExCkT27bX/VPt6pXlykbyuUKgSc7szSf1/AAsNtA5EGVTdurBzDkAh4sV8vTk4U2QjsMq+zemJ6lK27JOc2kE1bHNbG/oAoVF4P3Lc6KHfmMEfEq3LrRRLwh6NVNytEELWkhoQ+g08LPiFvqLCeeDEutqa7cv/xZLbtDFWkwuLFXiUAUKrRJrcLlU6Z676qg0SbQRXv1hE9oeRJP4V2diHmjlzb0CbrDGx88oX+cmfWjCokeyyyayl8/BPivfuZRGQ0hcWsTlpeRXgBppS3E+phKzgRFqzC7Bp0yu1ZfYyfUKh9QiAZIi6eh7Tqz1/uCsyjBXU9OJDTogsZD0JGTZw2b1JEoqbJkT7SC+5xZFOxMwZfkqg0o86E/a/EziYJS2xVkeCDLFVV/vCCOzW6D7CKu2S/L7uhbPb5XYxDlshH/mSkS1tzGVk/y6Qy; _gcl_au=1.1.238118696.1634613364; g_state={"i_p":1634620567480,"i_l":1}; reseor=71692/200%2C194/200; sCurrentPlatformLocale=TW; ftv=%7B%22ftv%22%3A%2220211019031602%22%2C%22ltv%22%3A%2220211019031602%22%2C%22ep%22%3A9999%2C%22cntv%22%3A1%2C%22cntc%22%3A0%2C%22cntcs%22%3A0%2C%22fep%22%3A9999%2C%22vc%22%3A0%2C%22ctl%22%3A106%2C%22ctf%22%3A106%2C%22item%22%3A0%2C%22path%22%3A91534%2C%22path2%22%3A91534%7D; trv_dt_src={%22dateSource%22:22%2C%22dateRange%22:{%22arrival%22:{%22day%22:24%2C%22month%22:10%2C%22year%22:2021}%2C%22departure%22:{%22day%22:25%2C%22month%22:10%2C%22year%22:2021}}}; _yoid=89ca3b15-5c81-423c-814b-c3b546dcda49; _yosid=fc5c4b0a-2db3-42c9-986e-04e3f2053250; attrChannel=seo; sessionDuration=30000; gtmClickCount=true; RT="z=1&dm=www.trivago.com.tw&si=e23ea991-149d-40ab-a372-075e731d6017&ss=kuxil9db&sl=3&tt=44i&bcn=%2F%2F684d0d3e.akstat.io%2F"; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Oct+19+2021+11%3A31%3A41+GMT%2B0800+(%E5%8F%B0%E5%8C%97%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=6.20.0&isIABGlobal=false&hosts=&consentId=0c737b02-e9a0-4211-a8f2-d5ba02e29d69&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1&geolocation=TW%3BTPE&AwaitingReconsent=false; OptanonAlertBoxClosed=2021-10-19T03:31:41.236Z; firstpage=false; pageviewCount=2; _uetsid=e769eac0308a11ecae6fbbeb32a0526f; _uetvid=e76a3910308a11ecb88381ad56ce4ed5; edge_tid=0882dd417534e3d783b2d8155d; edge_tid_s=0882dd417534e3d783b2d8155d',
            'referer': 'https://www.trivago.com.tw/?aDateRange[arr]=2021-10-24&aDateRange[dep]=2021-10-25&aPriceRange[from]=0&aPriceRange[to]=0&iRoomType=7&aRooms[0][adults]=2&cpt2=71692/200&hasList=1&hasMap=0&bIsSeoPage=0&sortingId=1&slideoutsPageItemId=&iGeoDistanceLimit=20000&address=&addressGeoCode=&offset=0&ra=&overlayMode=',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
            'authority': 'www.trivago.com.tw',
            'method': 'POST',
            'path': '/graphql',
            'scheme': 'https',
            'content-type': 'application/json',
            'origin': 'https://www.trivago.com.tw',
            'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'x-trv-app-id': 'HS_WEB_APP',
            'x-trv-cst': '32046,38217,45104,45749,45766,46136,46164,46535,47828,47908,48405,48506,48508,48542,48681,49291,49382,49419,49696,49752,49777,50553,50567,50805,50950,51032,51076,51246,51458,51591,51619,51886,51913,52217,52219,52345,52366,52551,52590,52756,52830,52891,52949,53005,53018,53183,53192,53231,53393,53508,53513,53593,53687,53852,53894,54061,54244,54273,54333,54362,54596,54827,54858,54889,54999,55003,55113,55133,55134,55136,55145,55353,55451,55628,55690,55739,55866,56275-3,56467-1,56477,56578,56633,56861-3,56937-2,57155,57488,57889-2,58038,58131,58205,58433',
            'x-trv-language': 'zh-Hant-TW',
            'x-trv-platform': 'tw',
            'x-trv-tid': '0882dd417534e3d783b2d8155d',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'apollographql-client-name': 'hs-web',
            'apollographql-client-version': 'v93_10_5_ae_f07e1e495a0'
            }
            ip = random.choice(m)
            proxies = {'http':"http://{}:{}@{}".format('vvbocpqj','obt7b7ug0dim',ip)}
            response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
            result = response.json()
            resulthotel = result['data']['rs']
            a = dateTodate.split('/')
            resulthotel['dataCreateTime'] = str(date.today())
            resulthotel['dataQueryTime'] = a[0]
            resulthotel['dataArrLoc'] = locLN1
            count+=25
            print(str(count)+" "+str(dateTodate)+" ip is "+str(ip))
            mycollection.insert_one(resulthotel)
        except Exception as e:
            print("ERROR:", url, e)
# getHotel("139.760330/35.666718","71462","20211024/20211025")
def getJPhotelSigleTh(date):
    next1 = date + timedelta(days=1)
    a = next1.strftime("%Y%m%d")
    b = date.strftime("%Y%m%d")
    for items in param.locLN:
        getHotel(str(param.locLN[items][0]),str(param.locLN[items][1]), "{}/{}".format(b,a))
        print("ok, {} {}".format(items,b))
        time.sleep(random.randint(1,5))
    print('------finish-------'+date)

def getJPhotelSigleThNoSave(date):
    next1 = date + timedelta(days=1)
    a = next1.strftime("%Y%m%d")
    b = date.strftime("%Y%m%d")
    for items in param.locLN:
        getHotelNoSave(str(param.locLN[items][0]),str(param.locLN[items][1]), "{}/{}".format(b,a))
        print("ok, {} {}".format(items,b))
        time.sleep(random.randint(1,5))
    print('------finish-------')
getJPhotelSigleThNoSave(date.today())
for i in range(1,19):
    start_date = date.today()+timedelta(5*(i-1))
    end_date = date.today()+ timedelta(5*i)
    datelist = [ single_date for single_date in daterange(start_date, end_date)]
    
        
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        
        executor.map(getJPhotelSigleTh, datelist)

    end_time = time.time()
    print(f"{end_time - start_time} 秒爬取, now i is at "+str(i))
    time.sleep(200)
    start_date = date.today()+timedelta(5*(i))
    end_date = date.today()+ timedelta(5*(i+1))
    datelistNoSave = [ single_date for single_date in daterange(start_date, end_date)]
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        
        executor.map(getJPhotelSigleThNoSave, datelistNoSave)
    time.sleep(200)





# for item in data:
#     proxyList.append(item['ip']+":"+item['port'])
# validIP=[]
# for ip in m:
#     try:
#         proxies = {'http':"http://{}:{}@{}".format('vvbocpqj','obt7b7ug0dim',ip)}
#         res = requests.get('https://api.ipify.org?format=json',proxies= proxies, timeout=5)
#         validIP.append({'ip':ip})
#         print(ip)
#     except:
#         print('FAIL',proxies)
# print(validIP)
# print(len(validIP))