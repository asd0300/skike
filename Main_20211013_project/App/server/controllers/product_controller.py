import re,requests
from datetime import  datetime,timedelta,date
import json
import os
import random
##########
import sys
from collections import defaultdict

import pymysql
from flask import jsonify, render_template, request
from pymongo import MongoClient
from server import app
from server.models.product_model import get_products, get_products_variants
from werkzeug.utils import secure_filename

from jinja2 import Template
from itertools import count

sys.path[0] += '\\..'
from env import config

PAGE_SIZE = 6
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

@app.route('/')
@app.route('/admin/main.html', methods=['GET'])
def main_index():
    return render_template('skike_flight.html')



def find_airticket(destination, paging):
    if (destination == 'all') :
        return get_products(PAGE_SIZE, paging, {"destination": destination})
    elif (destination in ['men', 'women', 'accessories']):
        return get_products(PAGE_SIZE, paging, {"destination": destination})
    elif (destination == 'search'):
        keyword = request.values["keyword"]
        if (keyword):
            return get_products(PAGE_SIZE, paging, {"keyword": keyword})


def get_products_with_detail(url_root, products):
    product_ids = [p["id"] for p in products]
    variants = get_products_variants(product_ids)
    variants_map = defaultdict(list)
    for variant in variants:
        variants_map[variant["product_id"]].append(variant)

    def parse(product, variants_map):
        product_id = product["id"]
        image_path = url_root + 'static/assets/' + str(product_id) + '/'
        product["main_image"] = image_path + product["main_image"]
        product["images"] = [image_path + img for img in product["images"].split(',')]
        product_variants = variants_map[product_id]
        if (not product_variants):
            return product

        product["variants"] = [
            {
                "color_code": v["color_code"],
                "size": v["size"],
                "stock": v["stock"]
            }
            for v in product_variants
        ]
        colors = [
            {
                "code": v["color_code"],
                "name": v["color_name"]
            }
            for v in product_variants
        ]
        product["colors"] = list({c['code'] + c["name"]: c for c in colors}.values())
        product["sizes"] = list(set([
            v["size"]
            for v in product_variants   
        ]))

        return product

    return [
        parse(product, variants_map) for product in products
    ]


@app.route('/api/1.0/api_get_airticket/<category>', methods=['GET'])
def api_get_airticket(destination):
    paging = request.values.get('paging') or 0
    paging = int(paging)
    res = find_airticket(destination, paging)

    if (not res):
        return {"error":'Wrong Request'}

    products = res.get("products")
    product_count = res.get("product_count")

    if (not products):
        return {"error":'Wrong Request'}
    
    if (not len(products)):
        if (destination == 'details'):
            return {"data": None}
        else:
            return {"data": []}

    products_with_detail = \
        get_products_with_detail(request.url_root, products) if products[0]["source"] == 'native' else products
    if (destination == 'details'):
        products_with_detail = products_with_detail[0]

    result = {}
    if (product_count > (paging + 1) * PAGE_SIZE):
        result = {
            "data": products_with_detail,
            "next_paging": paging + 1
        } 
    else: 
        result = {"data": products_with_detail}
    
    return result

@app.route('/api/1.0/products/<category>', methods=['GET'])
def api_get_products(category):
    paging = request.values.get('paging') or 0
    paging = int(paging)
    res = find_airticket(category, paging)

    if (not res):
        return {"error":'Wrong Request'}

    products = res.get("products")
    product_count = res.get("product_count")

    if (not products):
        return {"error":'Wrong Request'}
    
    if (not len(products)):
        if (category == 'details'):
            return {"data": None}
        else:
            return {"data": []}

    products_with_detail = \
        get_products_with_detail(request.url_root, products) if products[0]["source"] == 'native' else products
    if (category == 'details'):
        products_with_detail = products_with_detail[0]

    result = {}
    if (product_count > (paging + 1) * PAGE_SIZE):
        result = {
            "data": products_with_detail,
            "next_paging": paging + 1
        } 
    else: 
        result = {"data": products_with_detail}
    
    return result

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def save_file(folder, file):
    folder_root = app.root_path + app.config['UPLOAD_FOLDER']
    folder_path = folder_root + '/' + folder
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(
            folder_path,
            filename
        ))
        return filename
    else:
        return None

@app.route('/api/1.0/ticket', methods=['GET'])
def api_create_ticket():
    rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
                            user="admin",password=config.RDSMASTERPASSWORD,\
                            port=3306,database="skike",\
                            cursorclass = pymysql.cursors.DictCursor)
    cursor = rdsDB.cursor()
    conn = MongoClient("mongodb://localhost:{}/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false".format(config.MONGO_PASS_SKIKE_LOCAL))
    mydatabase = conn['skike'] 
    # Access collection of the database 
    mycollection=mydatabase['(2021-10-23)skike_ticket_to_JP']
    # mycollection=mydatabase['(2021-10-23)_ticket_to_Taiwan']
    # mycollection=mydatabase['(2021-10-25)skike_ticket_to_JP_child']
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
        # nowTime = int(time.time())
        for product in i['productInfoList']:
            duration_hour = product["durationInfo"]['hour'] #int 20
            duration_min = product["durationInfo"]['min'] #int 5
            # avbTickets = product["avbTickets"] #int 9
            # dDateTime = product["dDateTime"] #int 1641300000
            # aDateTime = product["aDateTime"] #1641375900
            filter_info_list_depart_time = product["filterInfoList"][0]['dTimeStr'] #str
            filter_info_list_arrive_time = product["filterInfoList"][0]['aTimeStr']+"+{}d".format(str(product['arrivalDays'])) #str
            flight_info_list = product["flightInfoList"] #list
            # print(flight_info_list)
            depart_city = flight_info_list[0]['dCityInfo']['name']
            arrive_city = flight_info_list[-1]['aCityInfo']['name']
            # print(flight_info_list[0]['dCityInfo']['name'])
            # print(flight_info_list[-1]['aCityInfo']['name'])
            stopover_minutes = product["stopoverMinute"] #int 960
            flight_info_list = product["flightInfoList"]
            # dataCreateTime = i["dataCreateTime"]
            data_query_time = i["dataQueryTime"]
            # shoppingId = str(dDateTime)+str(airplane_company_name)+str(aDateTime)
            
            #8000000118H4Z2dR0a1YGn800000000020000000000101V_m510G000O8YwW02Gx0800MTiYGmXL
            # if product['policyInfoList'][0]['priceDetailInfo']['adult'] != None:
            #     flightPriceAdult = product['policyInfoList'][0]['priceDetailInfo']['adult']['totalPrice'] #int
            #     # print(flightPriceAdult)
            # if product['policyInfoList'][0]['priceDetailInfo']['child'] != None:
            #     flightPriceChild = product['policyInfoList'][0]['priceDetailInfo']['child']['totalPrice'] #int
            #     # print(flightPriceChild)
            total_price = product['policyInfoList'][0]['priceDetailInfo']['viewTotalPrice']
            policy_info_list = product['policyInfoList']
            # print(policy_info_list)
            # print(shoppingId)
        
            for item in flight_info_list:
                terninal_arrive_time = item['aDateTime']#str
                # print(terninal_arrive_time)
                terninal_depart_city = str(item['dCityInfo']['name'])+" "+str(item['dPortInfo']['code'])+" "+\
                    str(item['dPortInfo']['name'])+" "+str(item['dPortInfo']['terminal']) #台北 TPE 桃園機場
                # print(terninal_depart_city)
                terninal_arrive_city = str(item['aCityInfo']['name'])+" "+str(item['aPortInfo']['code'])+" "+\
                    str(item['aPortInfo']['name'])+" "+str(item['aPortInfo']['terminal']) #台北 TPE 桃園機場
                # print(terninal_arrive_city)
                flight_company_and_number = str(item['airlineInfo']['name'])+" "+str(item['flightNo']) #真航空 LJ211
                # print(flight_company_and_number)
                flight_type_class = str(item['craftInfo']['name'])+" "+str(product['policyInfoList'][0]['productClass'][0]) #波音737-800 經濟艙
                # print(flight_type_class)
                stayover_times = str(product["filterInfoList"][0]['stopType'])+"個中轉站"# 1個中轉站 str
                # print(stayover_times)
                stayover_airport = str(item['dPortInfo']['code'])+'-'+str(stayover_times)+'-'+str(item['aPortInfo']['code'])# ICN-1個中轉站-KIX str
                # print(stayover_airport)
                airplane_company_name = str(item['airlineInfo']['name']) #真 航空
                shoppingId = product['policyInfoList'][0]['productKeyInfo']['shoppingId']
            # duratime = str(duration_hour)+"小時"+str(duration_min)+"分鐘"
            # shoppingId = str(dDateTime)+str(airplane_company_name)+str(aDateTime)
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
            sql_flyticket = "INSERT INTO skike.flight_ticket (`id`, `depart_city`, `arrive_City`, `data_query_time`, `duration_min`, `depart_time`, `arrive_time`, `stopover_minutes`, `aircraft_registration`, `stayover_times`, `flight_company`, `category`)VALUES (%s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            try:                    
                cursor.execute(sql_flyticket, (id, depart_city, arrive_City, data_query_time, duration_min, depart_time, arrive_time, stopover_minutes, aircraft_registration, stayover_times, flight_company, category))
                rdsDB.commit()
            except Exception as e:
                print("Exeception occured:{}".format(e))

            for item in flight_info_list:
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


                sql_stopover = "INSERT INTO skike.flight_stopover (`terminal_arrive_time`, `flight_depart_terminal`, `flight_arrive_terminal`, `flight_id`)VALUES (%s, %s, %s, %s)"
                try:                    
                    cursor.execute(sql_stopover, (terminal_arrive_time, flight_depart_terminal, flight_arrive_terminal, shoppingId))
                    rdsDB.commit()
                except Exception as e:
                    print("Exeception occured:{}".format(e))
            
            if product['policyInfoList'][0]['priceDetailInfo']['adult'] != None:
                for policy_item in policy_info_list:
                    product_flag =  policy_item['productFlag'],
                    price = policy_item['priceDetailInfo']['viewTotalPrice'],
                    adult_price = str(policy_item['priceDetailInfo']['adult']['totalPrice']),
                    # "child_price":str(policy_item['priceDetailInfo']['child']['totalPrice']),
                    # "infantPrice":str(policy_item['priceDetailInfo']['infant']['totalPrice']),
                    flight_class = str(policy_item['productClass'][0]),
                    available_tickets = policy_item['availableTickets'],
                    flight_ticket_feature = str(policy_item['descriptionInfo']['productName']),
                    flight_category = str(policy_item['descriptionInfo']['productCategory']),
                    ticket_description = str(policy_item['descriptionInfo']['ticketDescription']),
                    flight_id = shoppingId

                    sql_flightprice = "INSERT INTO skike.flight_price (`product_flag`, `price`, `adult_price`, `flight_class`, `available_tickets`, `flight_ticket_feature`, `flight_category`, `ticket_description`, `flight_id`\
                    )VALUES (%s,  %s, %s, %s, %s, %s, %s, %s, %s)"
                    try:                    
                        cursor.execute(sql_flightprice, (product_flag, price, adult_price,  flight_class, available_tickets, flight_ticket_feature, flight_category, ticket_description, flight_id))
                        rdsDB.commit()
                    except Exception as e:
                        print("Exeception occured:{}".format(e))

            elif product['policyInfoList'][0]['priceDetailInfo']['child'] != None:
                for policy_item in policy_info_list:
                    product_Flag =  policy_item['productFlag']
                    view_total_price = policy_item['priceDetailInfo']['viewTotalPrice']
                    # adultPrice = str(policy_item['priceDetailInfo']['adult']['totalPrice']),
                    child_price = str(policy_item['priceDetailInfo']['child']['totalPrice'])
                    # "infantPrice":str(policy_item['priceDetailInfo']['infant']['totalPrice']),
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

@app.route('/api/1.0/flight/tokyo', methods=['GET'])
def tickets_tokyo():
    paging = request.args.get('paging')
    if paging == None or paging == '':
        paging = 0
    rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
                        user="admin",password=config.RDSMASTERPASSWORD,\
                        port=3306,database="skike",\
                        cursorclass = pymysql.cursors.DictCursor)
    cursor = rdsDB.cursor()
    # sql = "SELECT * FROM skike.flight_ticket where data_query_time ='{}' order by data_query_time asc LIMIT {},{}".\
    #     format('2021-10-24',str(int(paging)*6),6)
    sql = "SELECT * FROM skike.flight_ticket where data_query_time ='{}' order by data_query_time asc".\
        format('2021-10-24')
    cursor.execute(sql)
    sql_result = cursor.fetchall()
    # sql1 = [data for data in sql_result]
    # print(sql1) 
    sql_get =[]
    for data in sql_result:
        sql_sub = "SELECT distinct (price) FROM skike.flight_ticket INNER JOIN skike.flight_price on flight_ticket.id = flight_price.flight_id where flight_ticket.id = '{}';".format(data['id'])
        cursor.execute(sql_sub)
        result_sub = cursor.fetchall()
        data['alternative_flight'] = result_sub
        sql_get.append(data)
    return render_template('skike_flight.html', flight_list=sql_get)


@app.route('/api/1.0/hotel', methods=['GET'])
def api_create_hotel():
    rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
                            user="admin",password=config.RDSMASTERPASSWORD,\
                            port=3306,database="skike",\
                            cursorclass = pymysql.cursors.DictCursor)
    cursor = rdsDB.cursor()
    conn = MongoClient("mongodb://localhost:{}/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false".format(config.MONGO_PASS_SKIKE_LOCAL))
    mydatabase = conn['skike'] 
    # Access collection of the database 
    mycollection=mydatabase['(2021-10-28)skike_hotel_v2']
    # print(str(date.today().strftime('%Y%m%d')))
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
        '$match': {
            # 'dataQueryTime': "{}".format(str(date.today().strftime('%Y%m%d')))
            'dataQueryTime': "20211102"
        }
    }, {
        '$limit': 20
    }
    ]
    result =mycollection.aggregate(pipetest)
    results = [doc for doc in result]
    for i in results:
        data_list = []
        for hotel_product in i['accommodations']:
            hotel_id = hotel_product['id']['id']
            data_query_time = i['dataQueryTime']
            time_format ="%Y%m%d"
            try:
                data_query_time = datetime.strptime(data_query_time, time_format).date()
            except Exception as e:
                print("Exeception occured:{}".format(e))
            hotel_name = hotel_product['name']['value']
            hotel_category = hotel_product['accommodationType']['value']
            hotel_location =  hotel_product['locality']['value']
            hotel_image = hotel_product['images']['mainUri']
            hotel_geo_lat = hotel_product['geocode']['lat']
            hotel_geo_lng = hotel_product['geocode']['lng']
            data_list.append((hotel_id,data_query_time,hotel_name,hotel_category,hotel_location,hotel_image,hotel_geo_lat,hotel_geo_lng))
        sql_hotel = "INSERT INTO skike.hotel (`id`, `data_query_time`, `name`, `category`, `locality`, `image_url`, `geocode_lat`, `geocode_lng`)VALUES (%s, %s, %s, %s, %s, %s,%s,%s)"
        print("insert data")
        try:
            cursor.executemany(sql_hotel,data_list)
            rdsDB.commit()
        except Exception as e:
            print("Exeception occured:{}".format(e))

    sql = "SELECT id, data_query_time FROM skike.hotel"
    cursor.execute(sql)
    sql_all_hotel_id = cursor.fetchall()
    try:
        with open(r"C:\Users\Ben Fan\Desktop\skike\Main_20211013_project\Webshare 10 proxies.txt",) as f:
            # data = json.load(f)
            data = f.read()
            m=re.findall('\d+\.\d+\.\d+\.\d+:\d+',data)
            f.close()
            print(m)
    except Exception as e:
            print("Exeception occured:{}".format(e))
    url = "https://www.trivago.com.tw/graphql"
    for item in sql_all_hotel_id[0:10]:
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
            mycollection=mydatabase['({})hotel_detail_skike'.format(str(item['data_query_time']))]
            ip = random.choice(m)
            proxies = {'http':"http://{}:{}@{}".format('vvbocpqj','obt7b7ug0dim',ip)}
            response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
            result = response.json()
            print(str(item['data_query_time'])+" ip is "+str(ip))
            # mycollection.insert_one(result)
            # print(result)
            data_list_hotel_detail = []
            for hotel_product_detail in result['data']['getAccommodationDeals']['deals']:
                data_query_time = item['data_query_time']
                hotel_agency = hotel_product_detail['advertiser']['name']
                agency_logo = "https:"+str(hotel_product_detail['advertiser']['advertiserLogo']['url'])
                hotel_feature =""
                for features in hotel_product_detail['priceAttributes']:
                    if features["label"] != None:
                        hotel_feature+=features["label"]+", "
                hotel_feature+= hotel_product_detail['description']
                price = hotel_product_detail['price']
                hotel_url = "https://www.trivago.com.tw/"+str(hotel_product_detail['clickoutPath'])
                hotel_id = item['id']
                data_list_hotel_detail.append((data_query_time,hotel_agency, agency_logo, hotel_feature, price, hotel_url, hotel_id))
            sql_hotel_detail = "INSERT INTO skike.hotel_alternative (`data_query_time`,`hotel_agency`, `agency_logo`, `hotel_feature`, `price`, `hotel_url`, `hotel_id`)VALUES (%s,%s, %s, %s, %s, %s, %s)"
            try:
                cursor.executemany(sql_hotel_detail,data_list_hotel_detail)
                rdsDB.commit()
            except Exception as e:
                print("Exeception occured:{}".format(e))
        except Exception as e:
                print("ERROR:", url, e)
    return "Ok"


@app.route('/api/1.0/hotel/tokyo', methods=['GET'])
def get_api_hotel_tokyo():
    paging = request.args.get('paging')
    if paging == None or paging == '':
        paging = 0
    rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
                        user="admin",password=config.RDSMASTERPASSWORD,\
                        port=3306,database="skike",\
                        cursorclass = pymysql.cursors.DictCursor)
    cursor = rdsDB.cursor()
    sql = "SELECT * FROM skike.hotel inner join skike.hotel_alternative on hotel.id =hotel_alternative.hotel_id group by name;"
    cursor.execute(sql)
    sql_result = cursor.fetchall()
    sql_get =[]
    for data in sql_result:
        sql_sub = "SELECT * FROM skike.hotel inner join skike.hotel_alternative on hotel.id =hotel_alternative.hotel_id where hotel.id = '{}';".format(data['id'])
        cursor.execute(sql_sub)
        result_sub = cursor.fetchall()
        data['alternative_agency_price'] = result_sub
        sql_get.append(data)
        print(sql_get)
    return render_template('skike_ticket.html', hotel_list=sql_get)