from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

import requests,re,random
import json
import time
# import pandas as pd
from env import config
from pymongo import MongoClient
import concurrent.futures
###date generator
from datetime import date, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date' : days_ago(0,0,0,0,0),
    'email' : ['fan0300@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries' : 1,
    'retry_delay': timedelta(minutes =1)
}

dag = DAG(
    'trip_com_flight_KR_2hr',
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

def just_a_function():
    conn = MongoClient("mongodb://skike4:{}@ec2-18-191-175-148.us-east-2.compute.amazonaws.com:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false".format(config.MONGO_PASS_SKIKE_UBUNTU))


    mydatabase = conn['skike'] 
    # Access collection of the database 
    mycollection=mydatabase['({})skike_ticket_to_KR_2hr'.format(str(date.today()))]


    # with open('Webshare 10 proxies.txt') as f:
        # data = json.load(f)
        # data = f.read()
        # m=re.findall('\d+\.\d+\.\d+\.\d+:\d+',data)
        # f.close()
        # print(m)


    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)
    ####

    def test(position,date1):
        try:
            url = "https://hk.trip.com/flights/graphql/intlFlightListSearchAll"

            payload = json.dumps({
            "operationName": "intlFlightListSearch",
            "variables": {
                "request": {
                "Head": {
                    "Currency": "TWD",
                    "ExtendFields": {
                    "SpecialSupply": "false"
                    }
                },
                "mode": 0,
                "searchNo": 1,
                "criteriaToken": "",
                "productKeyInfo": None,
                "searchInfo": {
                    "tripType": "OW",
                    "cabinClass": "YS",
                    "searchSegmentList": [
                    {
                        "dCityCode": "TPE",
                        "aCityCode": "{}".format(position),
                        "dDate": "{}".format(date1)
                    }
                    ],
                    "travelerNum": {
                    "adult": 1,
                    "child": 0,
                    "infant": 0
                    },
                    "openRtMergeSearch": False
                }
                }
            },
            "extensions": {
                "persistedQuery": {
                "version": 1,
                "sha256Hash": "d1d4e8962c73c4adc3a0f667f315b550f1d4f1228ad264da65e6aa51110d21a8"
                }
            }
            })
            headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'referer': 'https://hk.trip.com/flights/taibei-to-osaka/tickets-tpe-osa?FlightWay=OW&class=Y&Quantity=1&ChildQty=0&BabyQty=0&dcity=tpe&acity=osa&ddate=2022-01-04',
            'cookie': 'cookiePricesDisplayed=TWD; _abtest_userid=c9a403a4-5a35-4ac9-b77e-cda4d88ab996; _gcl_au=1.1.22915204.1634111486; _RSG=kVaUkRhJm2DYFZYojM.Dl8; _RDG=28bff0fb631abf2dcb1bb119dc6b6dfdc5; _RGUID=d0b04eb6-ee7a-47ee-8bcd-f96b728a33e2; g_state={"i_p":1634118692218,"i_l":1}; intl_ht1=h4%3D219_6112682; hotel=26562709; _uetvid=ecbdcf902cb511eca0e9a92191716a1b; ibulanguage=HK; ibulocale=zh_hk; _gid=GA1.2.449869172.1634461177; _dc_gtm_UA-109672825-6=1; IBU_FLT_HEAD_INFO=T_X8codPi-7T8IUICcpdEQ==; ibu_online_permission_cls_ct=2; ibu_online_permission_cls_gap=1634461178358; _gat_UA-109672825-3=1; _RF1=1.200.7.185; _ga=GA1.2.1003449919.1634111485; Union=AllianceID=1272710&SID=3456924&OUID=WegoAdsTW_CU&SourceID=&AppID=&OpenID=&Expires=1637053193499&createtime=1634461193; _bfi=p1%3D10320667452%26p2%3D10320667452%26v1%3D33%26v2%3D32; _ga_X437DZ73MR=GS1.1.1634461176.3.1.1634461217.0; _bfa=1.1634111485004.3fwpku.1.1634190707725.1634461176247.3.34; _bfs=1.27; _combined=transactionId%3D683516db-7d43-411f-8bea-4f10e4fec799%26usedistributionchannels%3DTrue%26channel%3DTWSite%26uuid%3D66b1b131-266b-4591-9f74-fe4cce2f705b; cookiePricesDisplayed=TWD; ibulanguage=HK; ibulocale=zh_hk; IBU_FLT_HEAD_INFO=T_X8codPi-7T8IUICcpdEQ==',
            'Content-Type': 'application/json'
            }
            ip = random.choice(m)
            proxies = {'http':"http://{}:{}@{}".format('vvbocpqj','obt7b7ug0dim',ip)}
            response = requests.request("POST", url, headers=headers, data=payload,proxies=proxies)
            print("OK------------------position "+str(position)+" date "+date1+" "+proxies['http'])
            # print(response)
            result = response.json()
            print(result['data']['intlFlightListSearch']['lowestPrice'])
            resultflight = result['data']['intlFlightListSearch']
            resultflight['dataCreateTime'] = str(date.today())
            resultflight['dataQueryTime'] = date1
            # print(resultflight[0])
            # for flightInfoList, stopoverPeriod in resultflight:
            #     print(stopoverPeriod['stopoverPeriod'] ,flightInfoList['flightInfoList'])
            
            # print(resultflight['flightInfoList'])
            # print(resultflight['durationInfo'])
        except Exception as e:
            print("ERROR:", url, e)
        
        try:
            mycollection.insert_one(resultflight)
        except Exception as e:
            print("ERROR:", url, e)




    jpList = ['北海道','尾花澤市','東京','大阪','京都','箱根','和歌山市','金澤','小樽','別府','長崎','宮古島']#查機場,城市名
    cityFList = ['OBO', 'MSJ', 'KMQ', 'NGS', 'HKD', 'TYO', 'TSJ', 'SHM', 'AKJ', 'OKI', 'IBR', 'KUH', 'NGO', 'MMY', 'FUJ', 'TAK', 'IKI', 'SPK', 'SHI', 'OSA']
    cityFList_KR = ['SEL', 'PUS', 'CJU', 'TAE', 'USN', 'KPO', 'HIN', 'RSU', 'YNY','WJU', 'KUV', 'KWJ', 'MWX']
    jpAirport = ['ITM', 'OKD', 'MSJ', 'KMQ', 'OKI', 'TSJ', 'NRT', 'CTS', 'HND', 'UKB', 'NGO', 'SHI', 'SHM', 'IKI', 'MMY', 'FUJ', 'NGS', 'KIX']
    # for item in jpAirport:   
    #     test(item)
    #     print(item)
    #     time.sleep(3)

    def getJPticketpage(date1):
        for item in cityFList_KR:   
            test(item, date1)
            time.sleep(random.randint(1,5))
        print('------finish-------'+date1)
    for i in range(1,4):
        start_date = date.today()+timedelta(30*(i-1))
        end_date = date.today()+ timedelta(30*i)
        datelist = [ single_date.strftime("%Y-%m-%d") for single_date in daterange(start_date, end_date)]



        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            
            executor.map(getJPticketpage, datelist)

        end_time = time.time()
        print(f"{end_time - start_time} 秒爬取")
        time.sleep(120)
    # print(datelist)
    # def dateCrawler():
    #     for single_date in daterange(start_date, end_date):
    #         start_time = time.time()
    #         end_time = time.time()
    #         print("--- %s seconds ---" % (end_time - start_time))
    # dateCrawler()

    conn = MongoClient("mongodb://skike4:{}@ec2-18-191-175-148.us-east-2.compute.amazonaws.com:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false".format(config.MONGO_PASS_SKIKE_UBUNTU))

    mydatabase = conn['skike'] 
    # Access collection of the database 
    mycollection=mydatabase['({})_ticket_to_Taiwan_from_KR_2hr'.format(str(date.today()))]


    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)
    ####

    def test(strat_position,arrive_position,date1):
        try:
            url = "https://hk.trip.com/flights/graphql/intlFlightListSearchAll"

            payload = json.dumps({
            "operationName": "intlFlightListSearch",
            "variables": {
                "request": {
                "Head": {
                    "Currency": "TWD",
                    "ExtendFields": {
                    "SpecialSupply": "false"
                    }
                },
                "mode": 0,
                "searchNo": 1,
                "criteriaToken": "",
                "productKeyInfo": None,
                "searchInfo": {
                    "tripType": "OW",
                    "cabinClass": "YS",
                    "searchSegmentList": [
                    {
                        "dCityCode": "{}".format(strat_position),
                        "aCityCode": "{}".format(arrive_position),
                        "dDate": "{}".format(date1)
                    }
                    ],
                    "travelerNum": {
                    "adult": 1,
                    "child": 0,
                    "infant": 0
                    },
                    "openRtMergeSearch": False
                }
                }
            },
            "extensions": {
                "persistedQuery": {
                "version": 1,
                "sha256Hash": "d1d4e8962c73c4adc3a0f667f315b550f1d4f1228ad264da65e6aa51110d21a8"
                }
            }
            })
            headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'referer': 'https://hk.trip.com/flights/taibei-to-osaka/tickets-tpe-osa?FlightWay=OW&class=Y&Quantity=1&ChildQty=0&BabyQty=0&dcity=tpe&acity=osa&ddate=2022-01-04',
            'cookie': 'cookiePricesDisplayed=TWD; _abtest_userid=c9a403a4-5a35-4ac9-b77e-cda4d88ab996; _gcl_au=1.1.22915204.1634111486; _RSG=kVaUkRhJm2DYFZYojM.Dl8; _RDG=28bff0fb631abf2dcb1bb119dc6b6dfdc5; _RGUID=d0b04eb6-ee7a-47ee-8bcd-f96b728a33e2; g_state={"i_p":1634118692218,"i_l":1}; intl_ht1=h4%3D219_6112682; hotel=26562709; _uetvid=ecbdcf902cb511eca0e9a92191716a1b; ibulanguage=HK; ibulocale=zh_hk; _gid=GA1.2.449869172.1634461177; _dc_gtm_UA-109672825-6=1; IBU_FLT_HEAD_INFO=T_X8codPi-7T8IUICcpdEQ==; ibu_online_permission_cls_ct=2; ibu_online_permission_cls_gap=1634461178358; _gat_UA-109672825-3=1; _RF1=1.200.7.185; _ga=GA1.2.1003449919.1634111485; Union=AllianceID=1272710&SID=3456924&OUID=WegoAdsTW_CU&SourceID=&AppID=&OpenID=&Expires=1637053193499&createtime=1634461193; _bfi=p1%3D10320667452%26p2%3D10320667452%26v1%3D33%26v2%3D32; _ga_X437DZ73MR=GS1.1.1634461176.3.1.1634461217.0; _bfa=1.1634111485004.3fwpku.1.1634190707725.1634461176247.3.34; _bfs=1.27; _combined=transactionId%3D683516db-7d43-411f-8bea-4f10e4fec799%26usedistributionchannels%3DTrue%26channel%3DTWSite%26uuid%3D66b1b131-266b-4591-9f74-fe4cce2f705b; cookiePricesDisplayed=TWD; ibulanguage=HK; ibulocale=zh_hk; IBU_FLT_HEAD_INFO=T_X8codPi-7T8IUICcpdEQ==',
            'Content-Type': 'application/json'
            }

            ip = random.choice(m)
            proxies = {'http':"http://{}:{}@{}".format('vvbocpqj','obt7b7ug0dim',ip)}
            response = requests.request("POST", url, headers=headers, data=payload, proxies= proxies)
            print("OK------------------position "+str(strat_position)+" to "+str(arrive_position)+" date "+date1+" "+proxies['http'])
            # print(response)
            result = response.json()
            print(result['data']['intlFlightListSearch']['lowestPrice'])
            resultflight = result['data']['intlFlightListSearch']
            resultflight['dataCreateTime'] = str(date.today())
            resultflight['dataQueryTime'] = date1
            # print(result)
            # for flightInfoList, stopoverPeriod in resultflight:
            #     print(stopoverPeriod['stopoverPeriod'] ,flightInfoList['flightInfoList'])
            
            # print(resultflight['flightInfoList'])
            # print(resultflight['durationInfo'])
        except Exception as e:
            print("ERROR:", url, e)
        

        mycollection.insert_one(resultflight)






    cityFList = ['OBO', 'MSJ', 'KMQ', 'NGS', 'HKD', 'TYO', 'TSJ', 'SHM', 'AKJ', 'OKI', 'IBR', 'KUH', 'NGO', 'MMY', 'FUJ', 'TAK', 'IKI', 'SPK', 'SHI', 'OSA']
    cityFList_KR = ['SEL', 'PUS', 'CJU', 'TAE', 'USN', 'KPO', 'HIN', 'RSU', 'YNY','WJU', 'KUV', 'KWJ', 'MWX']
    jpAirport = ['ITM', 'OKD', 'MSJ', 'KMQ', 'OKI', 'TSJ', 'NRT', 'CTS', 'HND', 'UKB', 'NGO', 'SHI', 'SHM', 'IKI', 'MMY', 'FUJ', 'NGS', 'KIX']
    # for item in jpAirport:   
    #     test(item)
    #     print(item)
    #     time.sleep(3)
    def dateCrawlerBKTW(date1):
            for item in cityFList_KR:   
                test(item,'TPE', date1)
                time.sleep(random.randint(1,5))
            print('------finish-------'+date1) 
    for i in range(1,4):
        start_date = date.today()+timedelta(30*(i-1))
        end_date = date.today()+ timedelta(30*i)
        datelist = [ single_date.strftime("%Y-%m-%d") for single_date in daterange(start_date, end_date)]
        start_time = time.time()       
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            
            executor.map(dateCrawlerBKTW, datelist)

        end_time = time.time()
        print(f"{end_time - start_time} 秒爬取")
        time.sleep(120)

run_etl = PythonOperator(
    task_id='whole_trip_com_flight_etl',
    python_callable = just_a_function,
    dag = dag,
)

run_etl