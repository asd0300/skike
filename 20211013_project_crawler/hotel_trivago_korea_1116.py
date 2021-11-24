from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import time,re
import requests
import json,random
from pymongo import MongoClient
import concurrent.futures
from env import config
###date generator
from datetime import date, timedelta


####



default_args = {
    'owner': 'airflow2',
    'depends_on_past': False,
    'start_date' : days_ago(0,0,0,0,0),
    'email' : ['fan0300@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries' : 1,
    'retry_delay': timedelta(minutes =1)
}
dag = DAG(
    'trivago_hotel_KR_1116',
    default_args = default_args,
    description= 'Our first DAG with ETL process2',
    schedule_interval = timedelta(days = 1)
)
m = ['209.127.191.180:9279'
    ,'45.95.96.132:8691'
    ,'45.95.96.187:8746'
    ,'45.95.96.237:8796'
    ,'45.136.228.154:6209'
    ,'45.94.47.66:8110'
    ,'45.94.47.108:8152'
    ,'193.8.56.119:9183'
    ,'45.95.99.226:7786'
    ,'45.95.99.20:7580'
]

# with open('Webshare 10 proxies.txt') as f:
#     # data = json.load(f)
#     data = f.read()
#     m=re.findall('\d+\.\d+\.\d+\.\d+:\d+',data)
#     f.close()
#     print(m)


def just_a_function2():
    locLN={'tokyo':["139.760330/35.666718","71462"],'osaka':["135.502167/34.693737","71692"],'北海道':["142.712402/43.464615","394794"],'山形縣':["140.880081/38.467224","71412"],'京都':["135.768036/35.011635","71539"],\
        '箱根':["139.106934/5.232353","71269"],'和歌山市':["135.170807/34.230511","71788"],'金澤':["136.656204/36.561325","69971"],'小樽':["140.994659/43.190716","72163"],'別府':["131.492172/33.293922","70829"],\
        '長崎':["129.877670/32.750286","70807"],'宮古島':["125.281151/24.805490","387895"]}

    locHotelCOM={'東京':["726784","東京, 東京 (都), 日本","CITY","東京"],'大阪':["728660","大阪, 大阪府, 日本","CITY","大阪"]}

    locLN_KR={'首爾':["126.977966/37.566536","81393"],'釜山':["129.075638/35.179554","81491"],'濟州市':["126.531189/33.499622","394794"],'大邱廣域市':["128.601440/35.871433","81464"],'蔚山':["129.311356/35.538376","81494"],\
        '慶州':["129.224747/35.856171","81466"],'仁川':["126.705208/37.456257","81416"],'全州':["127.147949/35.824223","81521"],'水原市':["127.028603/37.263573","81412"],'江陵':["128.876053/37.751854","81421"],\
        '平昌':["128.389984/37.370476","81445"],'春川':["127.729973/37.881313","81420"]}

    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)


    conn = MongoClient("mongodb://skike4:Asd7788123@ec2-18-191-175-148.us-east-2.compute.amazonaws.com:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false")
    mydatabase = conn['skike'] 
    # Access collection of the database 
    mycollection=mydatabase['(2021-11-16)skike_hotel_KR']
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
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
        "authority": "www.trivago.com.tw",
        "method": "POST",
        "path": "/graphql",
        "scheme": "https",
        "content-type": "application/json",
        "origin": "https://www.trivago.com.tw",
        "sec-ch-ua": "\"Google Chrome\";v=\"95\", \"Chromium\";v=\"95\", \";Not A Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-trv-app-id": "HS_WEB_APP",
        "x-trv-cst": "32046,38217,45104,45749,45766,46136,46164,46535,47828,47908,48405,48506,48508,48542,48681,49291,49382,49419,49696,49752,49777,50553,50567,50805,50950,51032,51076,51246,51458,51591,51619,51886,51913,52217,52219,52345,52366,52551,52590,52756,52830,52891,52949,53005,53018,53183,53192,53231,53393,53508,53513,53593,53687,53852,53894,54061,54244,54273,54333,54362,54596,54827,54858,54889,54999,55003,55113,55133,55134,55136,55145,55353,55451,55628,55690,55739,55866,56275-3,56467-1,56477,56578,56633,56861-3,56937-2,57155,57488,57889-2,58038,58131,58205,58433",
        "x-trv-language": "zh-Hant-TW",
        "x-trv-platform": "tw",
        "x-trv-tid": "0882dd417534e3d783b2d8155d",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "apollographql-client-name": "hs-web",
        "apollographql-client-version": "v93_10_5_ae_f07e1e495a0"
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
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
            "authority": "www.trivago.com.tw",
            "method": "POST",
            "path": "/graphql",
            "scheme": "https",
            "content-type": "application/json",
            "origin": "https://www.trivago.com.tw",
            "sec-ch-ua": "\"Google Chrome\";v=\"95\", \"Chromium\";v=\"95\", \";Not A Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-trv-app-id": "HS_WEB_APP",
            "x-trv-cst": "32046,38217,45104,45749,45766,46136,46164,46535,47828,47908,48405,48506,48508,48542,48681,49291,49382,49419,49696,49752,49777,50553,50567,50805,50950,51032,51076,51246,51458,51591,51619,51886,51913,52217,52219,52345,52366,52551,52590,52756,52830,52891,52949,53005,53018,53183,53192,53231,53393,53508,53513,53593,53687,53852,53894,54061,54244,54273,54333,54362,54596,54827,54858,54889,54999,55003,55113,55133,55134,55136,55145,55353,55451,55628,55690,55739,55866,56275-3,56467-1,56477,56578,56633,56861-3,56937-2,57155,57488,57889-2,58038,58131,58205,58433",
            "x-trv-language": "zh-Hant-TW",
            "x-trv-platform": "tw",
            "x-trv-tid": "0882dd417534e3d783b2d8155d",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "apollographql-client-name": "hs-web",
            "apollographql-client-version": "v93_10_5_ae_f07e1e495a0"
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
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
                "authority": "www.trivago.com.tw",
                "method": "POST",
                "path": "/graphql",
                "scheme": "https",
                "content-type": "application/json",
                "origin": "https://www.trivago.com.tw",
                "sec-ch-ua": "\"Google Chrome\";v=\"95\", \"Chromium\";v=\"95\", \";Not A Brand\";v=\"99\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "x-trv-app-id": "HS_WEB_APP",
                "x-trv-cst": "32046,38217,45104,45749,45766,46136,46164,46535,47828,47908,48405,48506,48508,48542,48681,49291,49382,49419,49696,49752,49777,50553,50567,50805,50950,51032,51076,51246,51458,51591,51619,51886,51913,52217,52219,52345,52366,52551,52590,52756,52830,52891,52949,53005,53018,53183,53192,53231,53393,53508,53513,53593,53687,53852,53894,54061,54244,54273,54333,54362,54596,54827,54858,54889,54999,55003,55113,55133,55134,55136,55145,55353,55451,55628,55690,55739,55866,56275-3,56467-1,56477,56578,56633,56861-3,56937-2,57155,57488,57889-2,58038,58131,58205,58433",
                "x-trv-language": "zh-Hant-TW",
                "x-trv-platform": "tw",
                "x-trv-tid": "0882dd417534e3d783b2d8155d",
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "apollographql-client-name": "hs-web",
                "apollographql-client-version": "v93_10_5_ae_f07e1e495a0"
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
        for items in locLN_KR:
            getHotel(str(locLN_KR[items][0]),str(locLN_KR[items][1]), "{}/{}".format(b,a))
            print("ok, {} {}".format(items,b))
            time.sleep(random.randint(1,5))
        print('------finish-------'+date)

    def getJPhotelSigleThNoSave(date):
        next1 = date + timedelta(days=1)
        a = next1.strftime("%Y%m%d")
        b = date.strftime("%Y%m%d")
        for items in locLN_KR:
            getHotelNoSave(str(locLN_KR[items][0]),str(locLN_KR[items][1]), "{}/{}".format(b,a))
            print("ok, {} {}".format(items,b))
            time.sleep(random.randint(1,5))
        print('------finish-------')
    print('start')
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



run_etl = PythonOperator(
    task_id='whole_trivago_com_hotel_etlKR',
    python_callable = just_a_function2,
    dag = dag,
)

run_etl