from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from datetime import  datetime,timedelta
import json
import pymysql
###date generator
from datetime import timedelta
from env import config
import random,time
import  requests

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
    'hotel_compare_RDS_insert_DAG',
    default_args = default_args,
    description= 'Our first DAG with ETL process',
    schedule_interval = timedelta(days = 1)
)


def hotel_compare_RDS_insert_DAG():
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
    url = "https://www.trivago.com.tw/graphql"
    KR_land = ['首爾' ,'大邱廣域市' ,'蔚山' ,'慶州','仁川','全州','水原市','江陵','平昌','春川']
    rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
                            user="admin",password=config.RDSMASTERPASSWORD,\
                            port=3306,database="skike",\
                            cursorclass = pymysql.cursors.DictCursor)
    cursor = rdsDB.cursor()
    for land in KR_land:
        sql = "SELECT * FROM skike.hotel where locality = '{}' group by name order by hotel_rating_count desc limit 20;".format(land)
        cursor.execute(sql)
        sql_land_result = cursor.fetchall()
        for hotel_id in sql_land_result:
            sql_com ="SELECT * FROM skike.hotel where id = '{}'".format(hotel_id['id']);
            cursor.execute(sql_com)
            sql_all_hotel_id = cursor.fetchall()
            num =0
            while(len(sql_all_hotel_id)>num*10):
                print("now num is "+str(num))
                for item in sql_all_hotel_id[(4*num):(4*(num+1))]:
                    date_1 = datetime.strptime(item['data_query_time'], "%Y-%m-%d")
                    item_add_1 = date_1+ timedelta(days =1)
                    item_add_1 = item_add_1.date()
                    try:
                        payload = json.dumps({
                        "operationName": "getAccommodationDeals",
                        "variables": {
                            "accommodationDealsParams": {
                            "accommodationNsid": {
                                "id": item['id'],
                                "ns": 100
                            },
                            "stayPeriod": {
                                "arrival": "{}".format(str(item['data_query_time'])),
                                "departure": "{}".format(str(item_add_1))
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
                        print("No save& insert data_query_time"+str(item['data_query_time'])+str(item['name']+" ip is "+str(ip)))
                    except Exception as e:
                            print("ERROR:", url, e)
                for item in sql_all_hotel_id[(10*num):(10*(num+1))]:
                    date_1 = datetime.strptime(item['data_query_time'], "%Y-%m-%d")
                    item_add_1 = date_1+ timedelta(days =1)
                    item_add_1 = item_add_1.date()
                    try:
                        payload = json.dumps({
                        "operationName": "getAccommodationDeals",
                        "variables": {
                            "accommodationDealsParams": {
                            "accommodationNsid": {
                                "id": item['id'],
                                "ns": 100
                            },
                            "stayPeriod": {
                                "arrival": "{}".format(str(item['data_query_time'])),
                                "departure": "{}".format(str(item_add_1))
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
                        # conn = MongoClient("mongodb://localhost:{}/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false".format(config.MONGO_PASS_SKIKE_LOCAL))
                        # mydatabase = conn['skike'] 
                        # Access collection of the database 
                        # mycollection=mydatabase['({})hotel_detail_skike'.format(str(item['data_query_time']))]
                        ip = random.choice(m)
                        proxies = {'http':"http://{}:{}@{}".format('vvbocpqj','obt7b7ug0dim',ip)}
                        response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
                        result = response.json()
                        #trivago is serious in time rate 
                        time.sleep(random.randint(1,5))
                        print("data_query_time "+str(item['data_query_time'])+" "+str(item['name']+"  ip is "+str(ip)))
                        # mycollection.insert_one(result)
                        # print(result)
                        data_list_hotel_detail = []
                        ##修改取得的價格數量 list 至 10價格
                        for hotel_product_detail in result['data']['getAccommodationDeals']['deals'][0:10]:
                            try:
                                data_query_time = item['data_query_time']
                                hotel_agency = hotel_product_detail['advertiser']['name']
                                agency_logo = "https:"+str(hotel_product_detail['advertiser']['advertiserLogo']['url'])
                                hotel_feature =""
                                for features in hotel_product_detail['priceAttributes']:
                                    if features["label"] != None:
                                        hotel_feature+=features["label"]+", "
                                hotel_feature+= hotel_product_detail['description']
                                price = hotel_product_detail['price']
                                hotel_url = "https://www.trivago.com.tw"+str(hotel_product_detail['clickoutPath'])
                                hotel_id = item['id']
                                data_list_hotel_detail.append((data_query_time,hotel_agency, agency_logo, hotel_feature, price, hotel_url, hotel_id))
                                # print(data_list_hotel_detail)
                            except Exception as e:
                                print("Exeception occured:{}".format(e))
                        sql_hotel_detail = "INSERT INTO skike.hotel_alternative (`data_query_time`,`hotel_agency`, `agency_logo`, `hotel_feature`, `price`, `hotel_url`, `hotel_id`)VALUES (%s,%s, %s, %s, %s, %s, %s)"
                        try:
                            cursor.executemany(sql_hotel_detail,data_list_hotel_detail)
                            rdsDB.commit()
                            print("now finish {} {} total will be {}".format(land,10*num,len(sql_all_hotel_id)))
                        except Exception as e:
                            print("Exeception occured:{}".format(e))
                    except Exception as e:
                            print("ERROR:", url, e)
                num+=1
    return "Ok"

flight_data_insert1 = PythonOperator(
    task_id='insert_flight',
    python_callable = hotel_compare_RDS_insert_DAG,
    dag = dag,
)



flight_data_insert1