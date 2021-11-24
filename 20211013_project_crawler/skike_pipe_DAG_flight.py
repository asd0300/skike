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
from datetime import  datetime,timedelta,date
import pymysql
import urllib.parse


default_args = {
    'owner': 'airflow1',
    'depends_on_past': False,
    'start_date' : datetime(2021,11,22),
    'email' : ['fan0300@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries' : 1,
    'retry_delay': timedelta(minutes =1)
}
dag = DAG(
    'Skike_pipe_flight_ver2',
    default_args = default_args,
    description= 'Our first DAG with ETL process3',
    schedule_interval = '30 16 * * *'
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



def get_flight_ticket_mongo():
    conn = MongoClient("mongodb://skike4:{}@ec2-18-191-175-148.us-east-2.compute.amazonaws.com:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false".format(config.MONGO_PASS_SKIKE_UBUNTU))


    mydatabase = conn['skike'] 
    # Access collection of the database 
    mycollection=mydatabase['({})skike_ticket_to_KR'.format(str(date.today()+timedelta(hours=8)))]


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
            time.sleep(random.randint(1,2))
            print("OK------------------position "+str(position)+" date "+date1+" "+proxies['http'])
            # print(response)
            result = response.json()
            print(result['data']['intlFlightListSearch']['lowestPrice'])
            resultflight = result['data']['intlFlightListSearch']
            resultflight['dataCreateTime'] = str(date.today()+timedelta(hours=8))
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
    mycollection=mydatabase['({})_ticket_to_Taiwan_from_KR'.format(str(date.today()+timedelta(hours=8)))]


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
            time.sleep(random.randint(1,2))
            print("OK------------------position "+str(strat_position)+" to "+str(arrive_position)+" date "+date1+" "+proxies['http'])
            # print(response)
            result = response.json()
            print(result['data']['intlFlightListSearch']['lowestPrice'])
            resultflight = result['data']['intlFlightListSearch']
            resultflight['dataCreateTime'] = str(date.today()+timedelta(hours=8))
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

def flight_data_insert():
    rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
                            user="admin",password=config.RDSMASTERPASSWORD,\
                            port=3306,database="skike",\
                            cursorclass = pymysql.cursors.DictCursor)
    cursor = rdsDB.cursor()
    conn = MongoClient("mongodb://skike4:{}@ec2-18-191-175-148.us-east-2.compute.amazonaws.com:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false".format(config.MONGO_PASS_SKIKE_UBUNTU))
    mydatabase = conn['skike'] 
    mycollection=mydatabase['({})skike_ticket_to_KR'.format(str(date.today()+timedelta(hours=8)))]
    pipetest = [
    {
        '$match': {
            'lowestPrice': {
                '$ne': None
            }
        }
    }
    ]
    result =mycollection.aggregate(pipetest)
    results = [doc for doc in result]
    for i in results:
        lowest_price = i['lowestPrice']
        criteria_token = i['resultBasicInfo']['criteriaToken']
        for product in i['productInfoList']:
            duration_hour = product["durationInfo"]['hour'] #int 20
            duration_min = product["durationInfo"]['min'] #int 5
            filter_info_list_depart_time = product["filterInfoList"][0]['dTimeStr'] #str
            filter_info_list_arrive_time = product["filterInfoList"][0]['aTimeStr']+"+{}d".format(str(product['arrivalDays'])) #str
            flight_info_list = product["flightInfoList"] #list
            depart_city = flight_info_list[0]['dCityInfo']['name']+','+ flight_info_list[0]['dCityInfo']['code']
            arrive_city = flight_info_list[-1]['aCityInfo']['name']+','+ flight_info_list[-1]['aCityInfo']['code']
            stopover_minutes = product["stopoverMinute"] #int 960
            flight_info_list = product["flightInfoList"]
            data_query_time = i["dataQueryTime"]
            total_price = product['policyInfoList'][0]['priceDetailInfo']['viewTotalPrice']
            policy_info_list = product['policyInfoList']
        
            for item in flight_info_list:
                try:
                    terninal_arrive_time = item['aDateTime']#str
                    terninal_depart_city = str(item['dCityInfo']['name'])+" "+str(item['dPortInfo']['code'])+" "+\
                        str(item['dPortInfo']['name'])+" "+str(item['dPortInfo']['terminal']) #台北 TPE 桃園機場
                    terninal_arrive_city = str(item['aCityInfo']['name'])+" "+str(item['aPortInfo']['code'])+" "+\
                        str(item['aPortInfo']['name'])+" "+str(item['aPortInfo']['terminal']) #台北 TPE 桃園機場
                    flight_company_and_number = str(item['airlineInfo']['name'])+" "+str(item['flightNo']) #真航空 LJ211
                    flight_type_class = str(item['craftInfo']['name'])+" "+str(product['policyInfoList'][0]['productClass'][0]) #波音737-800 經濟艙
                    stayover_times = str(product["filterInfoList"][0]['stopType'])+"個中轉站"# 1個中轉站 str
                    stayover_airport = str(item['dPortInfo']['code'])+'-'+str(stayover_times)+'-'+str(item['aPortInfo']['code'])# ICN-1個中轉站-KIX str
                    airplane_company_name = str(item['airlineInfo']['name']) #真 航空
                    shoppingId = product['policyInfoList'][0]['productKeyInfo']['shoppingId']
                except Exception as e:
                    print("Exeception occured:{}".format(e))
            print(data_query_time)
            print("-------------------------")

            
            id =shoppingId
            depart_city = depart_city
            arrive_City = arrive_city
            data_query_time = data_query_time
            duration_hour =duration_hour 
            duration_min =int(duration_hour*60+duration_min)
            depart_time = filter_info_list_depart_time 
            arrive_time = filter_info_list_arrive_time 
            stopover_minutes = stopover_minutes 
            aircraft_registration = flight_type_class
            stayover_times = stayover_times
            flight_company = flight_company_and_number
            if product['policyInfoList'][0]['priceDetailInfo']['adult'] != None:
                category = "adult"
            elif product['policyInfoList'][0]['priceDetailInfo']['chile'] != None:
                category = "child"
            sql_flyticket = "INSERT INTO skike.flight_ticket (`id`,`criteria_token`,`lowest_price`, `depart_city`, `arrive_City`, `data_query_time`, `duration_min`, `depart_time`, `arrive_time`, `stopover_minutes`, `aircraft_registration`, `stayover_times`, `flight_company`, `category`)VALUES (%s,%s,%s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            try:                    
                cursor.execute(sql_flyticket, (id,criteria_token,lowest_price, depart_city, arrive_City, data_query_time, duration_min, depart_time, arrive_time, stopover_minutes, aircraft_registration, stayover_times, flight_company, category))
                rdsDB.commit()
            except Exception as e:
                print("Exeception occured:{}".format(e))

            for item in flight_info_list:
                try:
                    terminal_arrive_time =  item['aDateTime']
                    flight_depart_terminal =  str(item['dCityInfo']['name'])+" "+str(item['dPortInfo']['code'])+" "+\
                        str(item['dPortInfo']['name'])+" "+str(item['dPortInfo']['terminal'])
                    flight_arrive_terminal =  str(item['aCityInfo']['name'])+" "+str(item['aPortInfo']['code'])+" "+\
                        str(item['aPortInfo']['name'])+" "+str(item['aPortInfo']['terminal'])
                    flight_company_and_number =  str(item['airlineInfo']['name'])+" "+str(item['flightNo'])
                    flight_type_class = str(item['craftInfo']['name'])+" "+str(product['policyInfoList'][0]['productClass'][0])
                    stayover_times = str(product["filterInfoList"][0]['stopType'])+"個中轉站"
                    stayover_airport =  str(item['dPortInfo']['code'])+'-'+str(stayover_times)+'-'+str(item['aPortInfo']['code'])
                    airplane_company_name = str(item['airlineInfo']['name'])
                except Exception as e:
                    print("Exeception occured:{}".format(e))


                sql_stopover = "INSERT INTO skike.flight_stopover (`terminal_arrive_time`, `flight_depart_terminal`, `flight_arrive_terminal`, `flight_id`)VALUES (%s, %s, %s, %s)"
                try:                    
                    cursor.execute(sql_stopover, (terminal_arrive_time, flight_depart_terminal, flight_arrive_terminal, shoppingId))
                    rdsDB.commit()
                except Exception as e:
                    print("Exeception occured:{}".format(e))
            
            if product['policyInfoList'][0]['priceDetailInfo']['adult'] != None:
                for policy_item in policy_info_list:
                    product_flag =  policy_item['productFlag']
                    price = policy_item['priceDetailInfo']['viewTotalPrice']
                    remark_token_key = str(policy_item['remarkTokenKey'])
                    adult_price = str(policy_item['priceDetailInfo']['adult']['totalPrice'])
                    flight_class = str(policy_item['productClass'][0])
                    available_tickets = policy_item['availableTickets']
                    flight_ticket_feature = str(policy_item['descriptionInfo']['productName'])
                    flight_category = str(policy_item['descriptionInfo']['productCategory'])
                    ticket_description = str(policy_item['descriptionInfo']['ticketDescription'])
                    flight_id = shoppingId
                    shoppingId = policy_item['productKeyInfo']['shoppingId']
                    groupKey = policy_item['productKeyInfo']['groupKey']

                    # print(shoppingId)
                    # print(groupKey)
                    url = "https://hk.trip.com/flights/passenger?FlightWay=OW&class=Y&Quantity=1&ChildQty=0&BabyQty=0&dcity=&acity=&ddate=&"
                    criteriaToken =i['resultBasicInfo']['criteriaToken']
                    # print(remark_token_key)
                    remark_token_key = urllib.parse.quote_plus(remark_token_key)
                    criteriaToken = urllib.parse.quote_plus(criteriaToken)
                    shoppingId = urllib.parse.quote_plus(shoppingId)
                    groupKey = urllib.parse.quote_plus(groupKey)
                    a = "remarkTokenKey="+remark_token_key+"&"+"criteriaToken="+criteriaToken+"&"+"shoppingId="+shoppingId+"&"+"groupKey="+groupKey
                    # b = a.replace(":","%3A").replace("|","%7C").replace("^","%5E").replace(",","")
                    url+=a
                    # print(url)
                    sql_flightprice = "INSERT INTO skike.flight_price (`group_id`, `price`, `adult_price`, `flight_class`, `available_tickets`, `flight_ticket_feature`, `flight_category`, `ticket_description`, `flight_id`,`url`\
                    )VALUES (%s,  %s, %s, %s, %s, %s, %s, %s, %s,%s)"
                    try:                    
                        cursor.execute(sql_flightprice, (groupKey, price, adult_price,  flight_class, available_tickets, flight_ticket_feature, flight_category, ticket_description, flight_id, url))
                        rdsDB.commit()
                    except Exception as e:
                        print("Exeception occured:{}".format(e))

            elif product['policyInfoList'][0]['priceDetailInfo']['child'] != None:
                for policy_item in policy_info_list:
                    product_Flag =  policy_item['productFlag']
                    view_total_price = policy_item['priceDetailInfo']['viewTotalPrice']
                    child_price = str(policy_item['priceDetailInfo']['child']['totalPrice'])
                    product_class = str(policy_item['productClass'][0])
                    available_tickets = policy_item['availableTickets']
                    product_name = str(policy_item['descriptionInfo']['productName'])
                    product_category = str(policy_item['descriptionInfo']['productCategory'])
                    ticket_description = str(policy_item['descriptionInfo']['ticketDescription'])
                    flight_id = shoppingId

                    sql_flightpriceChild = "INSERT INTO skike.flightpriceChild (`product_Flag`,\
                    `view_total_price`, `child_price`, `product_class`, `available_tickets`, \
                    `product_name`, `product_category`, `ticket_description`, `flight_id`\
                    )VALUES (%s,  %s, %s, %s, %s, %s, %s, %s, %s)"
                    try:                    
                        cursor.execute(sql_flightpriceChild, (product_Flag, view_total_price, child_price, product_class, available_tickets, product_name, product_category, ticket_description, shoppingId))
                        rdsDB.commit()
                    except Exception as e:
                        print("Exeception occured:{}".format(e))
    return "Ok"


def flight_data_insert_back_TW():
    rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
                            user="admin",password=config.RDSMASTERPASSWORD,\
                            port=3306,database="skike",\
                            cursorclass = pymysql.cursors.DictCursor)
    cursor = rdsDB.cursor()
    conn = MongoClient("mongodb://skike4:{}@ec2-18-191-175-148.us-east-2.compute.amazonaws.com:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false".format(config.MONGO_PASS_SKIKE_UBUNTU))
    mydatabase = conn['skike'] 
    mycollection=mydatabase['({})_ticket_to_Taiwan_from_KR'.format(str(date.today()+timedelta(hours=8)))]
    pipetest = [
    {
        '$match': {
            'lowestPrice': {
                '$ne': None
            }
        }
    }
    ]
    result =mycollection.aggregate(pipetest)
    results = [doc for doc in result]
    for i in results:
        lowest_price = i['lowestPrice']
        criteria_token = i['resultBasicInfo']['criteriaToken']
        for product in i['productInfoList']:
            duration_hour = product["durationInfo"]['hour'] #int 20
            duration_min = product["durationInfo"]['min'] #int 5
            filter_info_list_depart_time = product["filterInfoList"][0]['dTimeStr'] #str
            filter_info_list_arrive_time = product["filterInfoList"][0]['aTimeStr']+"+{}d".format(str(product['arrivalDays'])) #str
            flight_info_list = product["flightInfoList"] #list
            depart_city = flight_info_list[0]['dCityInfo']['name']+','+ flight_info_list[0]['dCityInfo']['code']
            arrive_city = flight_info_list[-1]['aCityInfo']['name']+','+ flight_info_list[-1]['aCityInfo']['code']
            stopover_minutes = product["stopoverMinute"] #int 960
            flight_info_list = product["flightInfoList"]
            data_query_time = i["dataQueryTime"]
            total_price = product['policyInfoList'][0]['priceDetailInfo']['viewTotalPrice']
            policy_info_list = product['policyInfoList']
        
            for item in flight_info_list:
                try:
                    terninal_arrive_time = item['aDateTime']#str
                    terninal_depart_city = str(item['dCityInfo']['name'])+" "+str(item['dPortInfo']['code'])+" "+\
                        str(item['dPortInfo']['name'])+" "+str(item['dPortInfo']['terminal']) #台北 TPE 桃園機場
                    terninal_arrive_city = str(item['aCityInfo']['name'])+" "+str(item['aPortInfo']['code'])+" "+\
                        str(item['aPortInfo']['name'])+" "+str(item['aPortInfo']['terminal']) #台北 TPE 桃園機場
                    flight_company_and_number = str(item['airlineInfo']['name'])+" "+str(item['flightNo']) #真航空 LJ211
                    flight_type_class = str(item['craftInfo']['name'])+" "+str(product['policyInfoList'][0]['productClass'][0]) #波音737-800 經濟艙
                    stayover_times = str(product["filterInfoList"][0]['stopType'])+"個中轉站"# 1個中轉站 str
                    stayover_airport = str(item['dPortInfo']['code'])+'-'+str(stayover_times)+'-'+str(item['aPortInfo']['code'])# ICN-1個中轉站-KIX str
                    airplane_company_name = str(item['airlineInfo']['name']) #真 航空
                    shoppingId = product['policyInfoList'][0]['productKeyInfo']['shoppingId']
                except Exception as e:
                    print("Exeception occured:{}".format(e))
            print(data_query_time)
            print("-------------------------")

            
            id =shoppingId
            depart_city = depart_city
            arrive_City = arrive_city
            data_query_time = data_query_time
            duration_hour =duration_hour 
            duration_min =int(duration_hour*60+duration_min)
            depart_time = filter_info_list_depart_time 
            arrive_time = filter_info_list_arrive_time 
            stopover_minutes = stopover_minutes 
            aircraft_registration = flight_type_class
            stayover_times = stayover_times
            flight_company = flight_company_and_number
            if product['policyInfoList'][0]['priceDetailInfo']['adult'] != None:
                category = "adult"
            elif product['policyInfoList'][0]['priceDetailInfo']['chile'] != None:
                category = "child"
            sql_flyticket = "INSERT INTO skike.flight_ticket (`id`,`criteria_token`, `lowest_price`,`depart_city`, `arrive_City`, `data_query_time`, `duration_min`, `depart_time`, `arrive_time`, `stopover_minutes`, `aircraft_registration`, `stayover_times`, `flight_company`, `category`)VALUES (%s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            try:                    
                cursor.execute(sql_flyticket, (id, criteria_token, lowest_price,depart_city, arrive_City, data_query_time, duration_min, depart_time, arrive_time, stopover_minutes, aircraft_registration, stayover_times, flight_company, category))
                rdsDB.commit()
            except Exception as e:
                print("Exeception occured:{}".format(e))

            for item in flight_info_list:
                try:
                    terminal_arrive_time =  item['aDateTime']
                    flight_depart_terminal =  str(item['dCityInfo']['name'])+" "+str(item['dPortInfo']['code'])+" "+\
                        str(item['dPortInfo']['name'])+" "+str(item['dPortInfo']['terminal'])
                    flight_arrive_terminal =  str(item['aCityInfo']['name'])+" "+str(item['aPortInfo']['code'])+" "+\
                        str(item['aPortInfo']['name'])+" "+str(item['aPortInfo']['terminal'])
                    flight_company_and_number =  str(item['airlineInfo']['name'])+" "+str(item['flightNo'])
                    flight_type_class = str(item['craftInfo']['name'])+" "+str(product['policyInfoList'][0]['productClass'][0])
                    stayover_times = str(product["filterInfoList"][0]['stopType'])+"個中轉站"
                    stayover_airport =  str(item['dPortInfo']['code'])+'-'+str(stayover_times)+'-'+str(item['aPortInfo']['code'])
                    airplane_company_name = str(item['airlineInfo']['name'])
                except Exception as e:
                    print("Exeception occured:{}".format(e))


                sql_stopover = "INSERT INTO skike.flight_stopover (`terminal_arrive_time`, `flight_depart_terminal`, `flight_arrive_terminal`, `flight_id`)VALUES (%s, %s, %s, %s)"
                try:                    
                    cursor.execute(sql_stopover, (terminal_arrive_time, flight_depart_terminal, flight_arrive_terminal, shoppingId))
                    rdsDB.commit()
                except Exception as e:
                    print("Exeception occured:{}".format(e))
            
            if product['policyInfoList'][0]['priceDetailInfo']['adult'] != None:
                for policy_item in policy_info_list:
                    product_flag =  policy_item['productFlag']
                    price = policy_item['priceDetailInfo']['viewTotalPrice']
                    remark_token_key = str(policy_item['remarkTokenKey'])
                    adult_price = str(policy_item['priceDetailInfo']['adult']['totalPrice'])
                    flight_class = str(policy_item['productClass'][0])
                    available_tickets = policy_item['availableTickets']
                    flight_ticket_feature = str(policy_item['descriptionInfo']['productName'])
                    flight_category = str(policy_item['descriptionInfo']['productCategory'])
                    ticket_description = str(policy_item['descriptionInfo']['ticketDescription'])
                    flight_id = shoppingId
                    shoppingId = policy_item['productKeyInfo']['shoppingId']
                    groupKey = policy_item['productKeyInfo']['groupKey']

                    # print(shoppingId)
                    # print(groupKey)
                    url = "https://hk.trip.com/flights/passenger?FlightWay=OW&class=Y&Quantity=1&ChildQty=0&BabyQty=0&dcity=&acity=&ddate=&"
                    criteriaToken =i['resultBasicInfo']['criteriaToken']
                    # print(remark_token_key)
                    remark_token_key = urllib.parse.quote_plus(remark_token_key)
                    criteriaToken = urllib.parse.quote_plus(criteriaToken)
                    shoppingId = urllib.parse.quote_plus(shoppingId)
                    groupKey = urllib.parse.quote_plus(groupKey)
                    a = "remarkTokenKey="+remark_token_key+"&"+"criteriaToken="+criteriaToken+"&"+"shoppingId="+shoppingId+"&"+"groupKey="+groupKey
                    # b = a.replace(":","%3A").replace("|","%7C").replace("^","%5E").replace(",","")
                    url+=a
                    # print(url)
                    sql_flightprice = "INSERT INTO skike.flight_price (`group_id`, `price`, `adult_price`, `flight_class`, `available_tickets`, `flight_ticket_feature`, `flight_category`, `ticket_description`, `flight_id`,`url`\
                    )VALUES (%s,  %s, %s, %s, %s, %s, %s, %s, %s,%s)"
                    try:                    
                        cursor.execute(sql_flightprice, (groupKey, price, adult_price,  flight_class, available_tickets, flight_ticket_feature, flight_category, ticket_description, flight_id, url))
                        rdsDB.commit()
                    except Exception as e:
                        print("Exeception occured:{}".format(e))

            elif product['policyInfoList'][0]['priceDetailInfo']['child'] != None:
                for policy_item in policy_info_list:
                    product_Flag =  policy_item['productFlag']
                    view_total_price = policy_item['priceDetailInfo']['viewTotalPrice']
                    child_price = str(policy_item['priceDetailInfo']['child']['totalPrice'])
                    product_class = str(policy_item['productClass'][0])
                    available_tickets = policy_item['availableTickets']
                    product_name = str(policy_item['descriptionInfo']['productName'])
                    product_category = str(policy_item['descriptionInfo']['productCategory'])
                    ticket_description = str(policy_item['descriptionInfo']['ticketDescription'])
                    flight_id = shoppingId
                    sql_flightpriceChild = "INSERT INTO skike.flightpriceChild (`product_Flag`,\
                    `view_total_price`, `child_price`, `product_class`, `available_tickets`, \
                    `product_name`, `product_category`, `ticket_description`, `flight_id`\
                    )VALUES (%s,  %s, %s, %s, %s, %s, %s, %s, %s)"
                    try:                    
                        cursor.execute(sql_flightpriceChild, (product_Flag, view_total_price, child_price, product_class, available_tickets, product_name, product_category, ticket_description, shoppingId))
                        rdsDB.commit()
                    except Exception as e:
                        print("Exeception occured:{}".format(e))
    return "Ok"


def truncate_flight_table():
    rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
                            user="admin",password=config.RDSMASTERPASSWORD,\
                            port=3306,database="skike",\
                            cursorclass = pymysql.cursors.DictCursor)
    cursor = rdsDB.cursor()
    try:   
        cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
        cursor.execute('TRUNCATE TABLE skike.flight_stopover;')
        cursor.execute('TRUNCATE TABLE skike.flight_price;')
        cursor.execute('TRUNCATE TABLE skike.flight_ticket;')
        cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')
        rdsDB.commit()
    except Exception as e:
        print("Exeception occured:{}".format(e))



get_flight_ticket_mongo_task1 = PythonOperator(
    task_id='get_flight_ticket_mongo_task1',
    python_callable = get_flight_ticket_mongo,
    dag = dag,
)

truncate_flight_table_task1 = PythonOperator(
    task_id='truncate_flight_table_task1',
    python_callable = truncate_flight_table,
    dag = dag,
)

flight_data_insert_task1 = PythonOperator(
    task_id='flight_data_insert_task1',
    python_callable = flight_data_insert,
    dag = dag,
)

flight_data_insert_back_TW_task1 = PythonOperator(
    task_id='flight_data_insert_back_TW_task1',
    python_callable = flight_data_insert_back_TW,
    dag = dag,
)

get_flight_ticket_mongo_task1>>truncate_flight_table_task1>>flight_data_insert_task1>>flight_data_insert_back_TW_task1