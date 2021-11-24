import re,requests
from flask.helpers import url_for
from datetime import  datetime,timedelta,date
import json
import os
import random
import sys,time,jwt
from collections import defaultdict

import pymysql
from flask import render_template, request,redirect,flash,jsonify,make_response,session
from pymongo import MongoClient
from server import app
from server.models.product_model import get_products, get_products_variants,get_hotel_alter,get_flight_ticket_alter,get_hotel_more_pic
from werkzeug.security import generate_password_hash
from server.env import config
from jinja2 import Template
from itertools import count
import polyline
from googletrans import Translator
import bcrypt

app.secret_key = config.SECRET_KEY
SECRET_KEY = config.SECRET_KEY
# sys.path[0] += '\\..'
from ..env import config

PAGE_SIZE = 6
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])


KR_location_list = [k for k,v in config.locLN_KR.items()]
today = str(date.today())
tomorrow = str(date.today()+timedelta(days=1))


def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password.encode('utf8'), bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf8'), hashed_password.encode('utf8'))

@app.route('/')
@app.route('/admin/main_flight', methods=['GET'])
def main_index():
    email = session.get('email')  # 取session
    if email:
        print(session)
        flash("welcome!")
        login = True
        return render_template('main.html',KR_location_list = KR_location_list,today = today, tomorrow = tomorrow, login =login)
        # return 'welcome %s' % username
    else:
        return render_template('main.html',KR_location_list = KR_location_list,today = today, tomorrow = tomorrow)

@app.route('/sign_out')
def sign_out():
    session.pop('email')
    return redirect(url_for('main_index'))

@app.route('/admin/user_page/', methods=['GET'])
def user_page():
    email = session.get('email')  # 取session
    if email:
        # print(email)
        login = True
        print(123)
        rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
                        user="admin",password=config.RDSMASTERPASSWORD,\
                        port=3306,database="skike",\
                        cursorclass = pymysql.cursors.DictCursor)
        sql_favorite = "SELECT * FROM skike.user_favorite where email = '{}';".format(email)
        cursor = rdsDB.cursor()
        cursor.execute(sql_favorite)
        print(456)
        sql_favorite_result_hotel = cursor.fetchall()
        print(sql_favorite_result_hotel)
        print(789)
        return render_template('user_page.html',KR_location_list = KR_location_list,today = today, tomorrow = tomorrow, login =login,sql_favorite_result_hotel=sql_favorite_result_hotel,email=email)
        # return 'welcome %s' % username
    else:
        return redirect(url_for("user_sign_in"))

@app.route('/admin/main_hotel/', methods=['GET'])
@app.route('/admin/main_hotel/<string:message>', methods=['GET'])
def hotel_search_html(message=None):
    email = session.get('email')  # 取session
    if email:
        flash("welcome!")
        login = True
        if message:
            return render_template('skike_hotel_search.html',KR_location_list = KR_location_list,today = today, tomorrow = tomorrow, login =login,message=message)
        return render_template('skike_hotel_search.html',KR_location_list = KR_location_list,today = today, tomorrow = tomorrow, login =login)
        # return 'welcome %s' % username
    else:
        return redirect(url_for("user_sign_in"))
    # return render_template('skike_hotel_search.html',KR_location_list = KR_location_list,today = today, tomorrow = tomorrow)


# @app.route('/test', methods=['GET'])
# def test():
#     return render_template("index1.html")

# @app.route('/sweet_alert2', methods=['GET', 'POST'])
# def login():

#     try:
#         flash('')
#         print(1)
#     except Exception as e:
#         print("Exeception occured:{}".format(e))
#     return render_template("index1.html")




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




@app.route('/api/1.0/ticket', methods=['GET'])
def api_create_ticket():
    rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
                            user="admin",password=config.RDSMASTERPASSWORD,\
                            port=3306,database="skike",\
                            cursorclass = pymysql.cursors.DictCursor)
    cursor = rdsDB.cursor()
    conn = MongoClient("mongodb://skike4:{}@ec2-18-191-175-148.us-east-2.compute.amazonaws.com:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false".format(config.MONGO_PASS_SKIKE_UBUNTU))
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
        for product in i['productInfoList']:
            duration_hour = product["durationInfo"]['hour'] #int 20
            duration_min = product["durationInfo"]['min'] #int 5
            filter_info_list_depart_time = product["filterInfoList"][0]['dTimeStr'] #str
            filter_info_list_arrive_time = product["filterInfoList"][0]['aTimeStr']+"+{}d".format(str(product['arrivalDays'])) #str
            flight_info_list = product["flightInfoList"] #list
            depart_city = flight_info_list[0]['dCityInfo']['name']
            arrive_city = flight_info_list[-1]['aCityInfo']['name']
            stopover_minutes = product["stopoverMinute"] #int 960
            flight_info_list = product["flightInfoList"]
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
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    cursor.execute("TRUNCATE TABLE skike.hotel_alternative")
    cursor.execute("TRUNCATE TABLE skike.hotel")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    print("truncate finish, !!!!!!!!!please double check truncate running status")
    conn = MongoClient("mongodb://skike4:{}@ec2-18-191-175-148.us-east-2.compute.amazonaws.com:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false".format(config.MONGO_PASS_SKIKE_EC22))
    mydatabase = conn['skike'] 
    # Access collection of the database 
    # mycollection=mydatabase['({})skike_hotel_KR'.format(str(date.today()))]
    yesterday = date.today() - timedelta(days=1)
    print(yesterday)
    # mycollection=mydatabase['({})skike_hotel_KR'.format(yesterday)]
    mycollection=mydatabase['({})skike_hotel_KR'.format(str(date.today()))]
    # print(str(date.today().strftime('%Y%m%d')))
    pipe_total =[
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
        '$count': 'dataArrLoc'
    }
    ]
    result_count =mycollection.aggregate(pipe_total)
    result_count2 = [doc for doc in result_count]
    mongo_result_count = result_count2[0]['dataArrLoc']
    for num in range(0,mongo_result_count,50):
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
                '$skip': num
            }, {
                '$limit': 50
            }
        ]
        result =mycollection.aggregate(pipetest)
        print(1)
        results = [doc for doc in result]
        a=0
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
                try:
                    if hotel_product['conceptDistance']!=None:
                        for near_station_list in hotel_product['conceptDistance'][0:1]:
                            hotel_near_location = str(near_station_list['name']['value'])
                            hotel_near_location_meter =str(near_station_list['distance_meters'])
                    else:
                        hotel_near_location=""
                        hotel_near_location_meter=""
                        hotel_rating_count = hotel_product['rating']['basedOn']
                        hotel_rating_avg_score = hotel_product['rating']['formattedOverallLiking']
                        hotel_best_price_per_stay = hotel_product['deals']['bestPrice']['displayPricePerStay']
                        price_list= hotel_best_price_per_stay.split(',')
                        hotel_best_price_per_stay = price_list[0]+price_list[1]
                        hotel_best_price_per_stay = hotel_best_price_per_stay[3:]
                        hotel_category = hotel_product['accommodationType']['value']
                        hotel_location =  hotel_product['locality']['value']
                        hotel_image = hotel_product['images']['mainUri']
                        hotel_geo_lat = hotel_product['geocode']['lat']
                        hotel_geo_lng = hotel_product['geocode']['lng']
                        data_list.append((hotel_id,data_query_time,hotel_name,hotel_near_location,hotel_near_location_meter,hotel_rating_count,hotel_rating_avg_score,hotel_best_price_per_stay,hotel_category,hotel_location,hotel_image,hotel_geo_lat,hotel_geo_lng))
                except Exception as e:
                    print("Exeception occured:{}".format(e))
                sql_hotel = "INSERT INTO skike.hotel (`id`, `data_query_time`, `name`, `hotel_near_location`, `hotel_near_location_meter`, `hotel_rating_count`, `hotel_rating_avg_score`, `hotel_best_price_per_stay`, `category`, `locality`, `image_url`, `geocode_lat`, `geocode_lng`)VALUES (%s, %s, %s, %s, %s, %s,%s,%s,%s, %s, %s, %s, %s)"
                print("prepare insert data "+str(hotel_id)+" data_query_time "+str(data_query_time))
            try:
                cursor.executemany(sql_hotel,data_list)
                rdsDB.commit()
                a+=1
                print("now in "+str(a)+"total 50 ,mongo in "+str(num)+" total mongo is "+str(mongo_result_count))
            except Exception as e:
                print("Exeception occured:{}".format(e))
            
    return "ok" 
@app.route('/api/1.0/hotel/money_compare', methods=['GET'])
def api_create_hotel_compare_money():
    sql = "SELECT * FROM skike.hotel where locality in ( '首爾' ,'大邱廣域市' ,'蔚山' ,'慶州','仁川','全州','水原市','江陵','平昌','春川') order by hotel_rating_count desc limit 5000;"
    rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
                            user="admin",password=config.RDSMASTERPASSWORD,\
                            port=3306,database="skike",\
                            cursorclass = pymysql.cursors.DictCursor)
    cursor = rdsDB.cursor()
    cursor.execute(sql)
    sql_all_hotel_id = cursor.fetchall()
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
    # print("Exeception occured:{}".format(e))
    url = "https://www.trivago.com.tw/graphql"
    num =0
    while(len(sql_all_hotel_id)>num*20):
        for item in sql_all_hotel_id[(20*num):(20*(num+1))]:
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
                # conn = MongoClient("mongodb://localhost:{}/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false".format(config.MONGO_PASS_SKIKE_LOCAL))
                # mydatabase = conn['skike'] 
                # Access collection of the database 
                # mycollection=mydatabase['({})hotel_detail_skike'.format(str(item['data_query_time']))]
                ip = random.choice(m)
                proxies = {'http':"http://{}:{}@{}".format('vvbocpqj','obt7b7ug0dim',ip)}
                response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
                time.sleep(random.randint(1,5))
                result = response.json()
                print("data_query_time"+str(item['data_query_time'])+str(item['name']+" ip is "+str(ip)))
                # mycollection.insert_one(result)
                # print(result)
                data_list_hotel_detail = []
                for hotel_product_detail in result['data']['getAccommodationDeals']['deals']:
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
                    print("now finish {} total will be {}".format(20*num,len(sql_all_hotel_id)))
                except Exception as e:
                    print("Exeception occured:{}".format(e))
            except Exception as e:
                    print("ERROR:", url, e)
        num+=1
    return "Ok"
@app.route('/admin/user', methods=['GET'])
def user_sign_up():
    return render_template('user_register.html')
@app.route('/admin/user_login', methods=['GET'])
def user_sign_in():
    return render_template('user_login.html')
@app.route('/user/sign_up', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':        
        user_details = request.form
        name = user_details['username']
        email = user_details['email']
        password = user_details['password']
        provider = "native"
        hashed_password = get_hashed_password(password)
        acceess_expire = 86400
        tokenSignUp = jwt.encode({'provider':provider,\
                                  'name':name,\
                                  'email': email }, SECRET_KEY)
        # tokenAfterDecode=tokenSignUp.decode('utf8').replace("'", '"')
        # tokenAfterDecode=tokenSignUp.decode('utf8').replace("'", '"')
        rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
                            user="admin",password=config.RDSMASTERPASSWORD,\
                            port=3306,database="skike",\
                            cursorclass = pymysql.cursors.DictCursor)
        cursor = rdsDB.cursor()
        query = 'SELECT * FROM skike.user where email = "{}";'.format(str(email))
        cursor.execute(query)
        sign_up_data = cursor.fetchone()
        rdsDB.commit()
        picture =""
        if sign_up_data:
            error = "A person with this email or name already exists, please try another email name"
            rdsDB.close()
            flash(error)
            return render_template('user_register.html',message = error)
        else:
            if provider =="native":
                try:
                    sign_up_data = "INSERT INTO `user` (`provider`, `name`,\
                                `email`, `password`, `picture`,\
                                `access_token`, `access_expired`) \
                                VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sign_up_data, (provider, name, email,\
                                hashed_password, picture, tokenSignUp,\
                                acceess_expire))
                except Exception as e:
                    print("Exeception occured:{}".format(e))
                rdsDB.commit()
                query = 'SELECT * FROM skike.user where email = "{}";'.format(str(email))
                cursor.execute(query)
                sign_up_after=cursor.fetchone()
                provider = "native"
                # token_Json =sign_up_after[6].decode('utf8').replace("'", '"')
                user_access = {'access_token':sign_up_after["access_token"], 'access_expired':sign_up_after['access_expired']}
                # user_access = {}
                user_content = {"id":sign_up_after['id'],"provider":sign_up_after['provider'],\
                                "name":sign_up_after['name'], "email":sign_up_after['email'],\
                                "picture":sign_up_after['picture']}
                rdsDB.commit()
                error = "Register Success!"
                tempA={"user":user_content}
                user_access.update(tempA)
            finalSignup = {"data":user_access}
        rdsDB.close()
        message ="Account create ok, please sign in again"
        return render_template('user_login.html',message=message)

@app.route('/user/sign_in', methods=['post'])
@app.route('/user/sign_in<message>', methods=['get'])
def login():
    """login"""
    if request.method == 'POST' :
        user_details = request.form
        email = user_details['email']
        password_form = user_details['password']
        # print(password_form)
        rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
                user="admin",password=config.RDSMASTERPASSWORD,\
                port=3306,database="skike",\
                cursorclass = pymysql.cursors.DictCursor)
        cursor = rdsDB.cursor()
        query = 'SELECT * FROM skike.user WHERE email = "{}" ;'.format(email)
        cursor.execute(query)
        sign_data = cursor.fetchone()
        # print(sign_data)
        rdsDB.commit()
        try:
            check_password(password_form, sign_data["password"])
        except Exception as e:
            print("Exeception occured:{}".format(e))
        
        if sign_data:
            if check_password(password_form, sign_data["password"]):
                session['email'] = email
                session['uid'] = random.randint(0, 100)
                # print(2)
                # sign_content = {'access_token':sign_data['access_token'], 'access_expired':sign_data['access_expired']}
                # print(sign_content)
                # user_content = {'id': sign_data['id'],"provider": sign_data['provider'],\
                #     "name": sign_data['name'],"email": sign_data['email'],\
                #     "picture": sign_data['picture']}
                # print(user_content)
                # userTemp = {"user":user_content}
                # sign_content.update(userTemp)
                # sign_data_final = {"data":sign_content}
                rdsDB.close()
            return redirect(url_for('main_index'))
        elif sign_data ==None:
            error = "Can't recognite this user/id please try again"
            rdsDB.close()
            flash(error)
            return render_template('user_login.html',message = error)
        error = "Can't search this user/id please try again"
    return render_template('user_login.html',message = error)

@app.route('/api/1.0/hotel/search/', methods=['POST','GET'])
def hotel_search():
    email = session.get('email')  # 取session
    if email:
        login = True
        # return 'welcome %s' % username

        form_data = request.form
        # print("this hotel")
        # print(form_data)
        # booking_category = form_data['booking_category']
        location = form_data['location']
        start_date = form_data['start_date']
        end_date = form_data['end_date']
        if start_date>end_date:
            message ="想搜尋日期不能大於日期結尾,請在搜尋一次"
            return redirect(url_for("hotel_search_html",message=message))
        # select_adult2 = form_data['adults_number']
        # select_rooms2 = form_data['rooms']
        paging = request.args.get('paging')
        if paging == None or paging == '':
            paging = 0
        rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
                            user="admin",password=config.RDSMASTERPASSWORD,\
                            port=3306,database="skike",\
                            cursorclass = pymysql.cursors.DictCursor)
        cursor = rdsDB.cursor()
        sql = "SELECT * FROM skike.hotel where DATE(hotel.data_query_time) BETWEEN '{}' AND '{}' group by name having locality like'{}' order by hotel_rating_count desc limit 1000".format(start_date,end_date,location)
        cursor.execute(sql)
        sql_result = cursor.fetchall()
        # print(sql_result)
        sql_count = "SELECT count(distinct(name)) FROM skike.hotel where DATE(hotel.data_query_time) BETWEEN '{}' AND '{}' AND locality ='{}' group by name;".format(start_date,end_date,location)
        cursor.execute(sql_count)
        sql_count_result = cursor.fetchall()
        sum = 0
        for item in sql_count_result:
            sum+=item['count(distinct(name))']
        return render_template('skike_hotel.html', hotel_list=sql_result, start_date= start_date, end_date = end_date, location = location,sum = sum,login =login)
    else:
        return redirect(url_for("user_sign_in"))
@app.route('/api/1.0/hotel/search/<location>', methods=['GET'])
def hotel_search_title_get(location):
    email = session.get('email')  # 取session
    if email:
        flash("welcome!")
        login = True
        # return 'welcome %s' % username
        start_date = date.today()
        end_date = date.today()+timedelta(7)
        method = "hotel_search_title_get"
        rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
                            user="admin",password=config.RDSMASTERPASSWORD,\
                            port=3306,database="skike",\
                            cursorclass = pymysql.cursors.DictCursor)
        cursor = rdsDB.cursor()
        sql = "SELECT * FROM skike.hotel where DATE(hotel.data_query_time) BETWEEN '{}' AND '{}' group by name having locality like'{}' order by hotel_rating_count desc limit 1000".format(start_date,end_date,location)
        cursor.execute(sql)
        sql_result = cursor.fetchall()
        sql_count = "SELECT count(distinct(name)) FROM skike.hotel where DATE(hotel.data_query_time) BETWEEN '{}' AND '{}' AND locality ='{}' group by name;".format(start_date,end_date,location)
        cursor.execute(sql_count)
        sql_count_result = cursor.fetchall()
        sum = 0
        for item in sql_count_result:
            sum+=item['count(distinct(name))']
        
        return render_template('skike_hotel.html', hotel_list=sql_result, start_date= start_date, end_date = end_date, location = location, method = method, sum =sum, login =login)
    else:
        return redirect(url_for("user_sign_in"))
@app.route('/route_function',methods=[ "GET",'POST'])
def route_function():
    rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
                    user="admin",password=config.RDSMASTERPASSWORD,\
                    port=3306,database="skike",\
                    cursorclass = pymysql.cursors.DictCursor)
    cursor = rdsDB.cursor()
    print(request.form)
    print(request.form.get('delete_user_page'))
    if request.form.get('delete_user_page'):
        email = session.get('email')
        hotel_name = request.form.get('hotel_name')
        sql_favorite = "DELETE FROM skike.user_favorite where email='{}' and hotel_name='{}'".format(email,hotel_name)
        try:
            cursor.execute(sql_favorite)
            rdsDB.commit()
            rdsDB.close()
        except Exception as e:
            print("Exeception occured:{}".format(e))
        return"ok"
    hotel_name = request.form.get('the_name')
    want_time_start = request.form.get('want_time_start')
    want_time_end = request.form.get('want_time_end')
    hotel_detail = request.form.get('hotel_detail')
    hotel_img = request.form.get('hotel_img')
    email = session.get('email')
    location = request.form.get('location')
    price = request.form.get('price')
    price =int(''.join([x for x in price if x.isdigit()]))
    user_name= "test"
    print(request.form.get('status'))
    favo_add_list = [(email,want_time_start,want_time_end,hotel_name,hotel_img,hotel_detail,user_name,location,price)]
    if request.form.get('status'):
        sql_favorite = "DELETE FROM skike.user_favorite where email='{}' and hotel_detail='{}' and hotel_img ='{}'".format(email,hotel_detail,hotel_img)
        try:
            cursor.execute(sql_favorite)
            rdsDB.commit()
            rdsDB.close()
        except Exception as e:
            print("Exeception occured:{}".format(e))
    else:
        sql_favorite = "INSERT INTO skike.user_favorite (`email`, `want_time_start`, `want_time_end`, `hotel_name`, `hotel_img`, `hotel_detail`, `name`,`location`,`price`)VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            cursor.executemany(sql_favorite,favo_add_list)
            rdsDB.commit()
            rdsDB.close()
        except Exception as e:
            print("Exeception occured:{}".format(e))
    return "ok"
@app.route('/hotel/search/more_picture',methods=[ "GET",'POST'])
def hotel_more_picture():
    print(request.form)
    hotel_id = request.form.get('hotel_id')
    want_time_start = request.form.get('want_time_start')
    want_time_end = request.form.get('want_time_end')
    print(hotel_id,want_time_start,want_time_end)
    pic_list = get_hotel_more_pic(hotel_id,want_time_start,want_time_end)
    # pic_list2 = ['<div class="row"><button id ="x_{}" ><img class ="pic_x"src="https://freesvg.org/img/close-button.png" width=30" height="30" style="border-radius: 10px; vertical-align: unset; margin-top:5px;float:right"/></button></div>'.format(hotel_id)]
    pic_list2=[]
    pic_list3=[]
    print(2)
    pic_list2.append('<div class="row"><button id ="x_{}" onclick="listBtn{}()"style="float: left; border: 1px solid #f6685e; font-size: 16px;      font-weight: 500; border-radius: 35px; color: #f6685e;      cursor: pointer; background-color: #f6685e; color: #fff;      z-index: 3; position: absolute; margin-left: 10%; margin-top: -39px;"/>關閉相片</button></div>'.format(hotel_id,hotel_id))
    a =0
    print(1)
    for url in pic_list[0:28]:
        pic_list3.append("<div class='col'><img src='{}' width='236' height='160' style='border-radius: 10px; vertical-align: unset; margin-top:5px'/></div>".format(url))
        a+=1
    pic_dict={}
    pic_dict['pic_list2'] = pic_list2
    pic_dict['pic_list3'] = pic_list3
    # print(pic_dict)
    print("___________________________")
    # print(pic_dict)
    # return "<p>123</p>"
    return pic_dict
@app.route('/api/1.0/hotel/search/<start_date>/<end_date>/<location>/<condition>', methods=['GET'])
def hotel_search_get(start_date,end_date,location,condition):
    print("thisiss")
    print(start_date,end_date,location,condition)
    condition1 = condition.split(',')
    condition1 = condition1[0]
    condition2 = condition.split(',')
    condition2 = condition2[1]
    print(condition1,condition2)
    # if request.form:
    #     form_data = request.form
    #     # print("this hotel")
    #     # print(form_data)
    #     # booking_category = form_data['booking_category']
    #     location = form_data['location']
    #     start_date = form_data['start_date']
    #     end_date = form_data['end_date']
    #     # select_adult2 = form_data['adults_number']
    #     # select_rooms2 = form_data['rooms']
    print(1)
    paging = request.args.get('paging')
    if paging == None or paging == '':
        paging = 0
    rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
                        user="admin",password=config.RDSMASTERPASSWORD,\
                        port=3306,database="skike",\
                        cursorclass = pymysql.cursors.DictCursor)
    cursor = rdsDB.cursor()
    sql = "SELECT * FROM skike.hotel where DATE(hotel.data_query_time) BETWEEN '{}' AND '{}' group by name having locality like'{}' order by {} {} limit 1000".format(start_date,end_date,location,condition1,condition2)
    cursor.execute(sql)
    sql_result = cursor.fetchall()
    return render_template('skike_hotel.html', hotel_list=sql_result, start_date= start_date, end_date = end_date, location = location)
@app.route('/api/1.0/air_plane/search_get', methods=['POST','GET'])   
def airplane_search_func():
    email = session.get('email')  # 取session
    if email:
        # flash("welcome!")
        login = True
        # return 'welcome %s' % username
        form_data = request.form
        # print(form_data)
        # booking_category = form_data['booking_category']
        round = form_data['round']
        location = form_data['location']
        location_arrive = form_data['location_arrive']
        start_date = form_data['start_date']
        # end_date = form_data['end_date']
        select_adult = form_data['adults_number']
        # select_rooms2 = form_data['rooms']
        # paging = request.args.get('paging')
        rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
                            user="admin",password=config.RDSMASTERPASSWORD,\
                            port=3306,database="skike",\
                            cursorclass = pymysql.cursors.DictCursor)
        cursor = rdsDB.cursor()
        # print(start_date)
        # sql = "SELECT * FROM skike.flight_ticket where data_query_time ='{}' order by data_query_time asc LIMIT {},{}".\
        #     format('2021-10-24',str(int(paging)*6),6)
        # sql = "SELECT * FROM skike.flight_ticket where data_query_time ='{}' order by data_query_time asc".\
        #     format('2021-10-24')
        # sql = "SELECT * FROM skike.flight_ticket where data_query_time ='{}' and arrive_City = '{}' and depart_city ='{}' order by data_query_time asc;".format(start_date,location_arrive,location)
        sql = "SELECT * FROM skike.flight_ticket where data_query_time ='{}' and  arrive_City = '{}' and depart_city ='{}';".format(start_date,location_arrive,location)
        cursor.execute(sql)
        sql_result = cursor.fetchall()
        # print(sql_result)
        #handle flight pic
        for sql_result_sub in sql_result:
            air_pic = sql_result_sub['flight_company'].split(' ')
            air_pic = air_pic[1]
            air_pic = air_pic[0:2]
            air_pic = "https://pic.tripcdn.com/airline_logo/3x/{}.webp".format(air_pic.lower())
            sql_result_sub['air_pic'] = air_pic
        #end flight pic
        
        # print(sql1) 
        sql_get =[]
        for data in sql_result:
            # print(data)
            depart_city = data['depart_city'].split(',')
            depart_city = depart_city[1]
            # print(depart_city)
            arrive_city = data['arrive_City'].split(',')
            arrive_city = arrive_city[1]
            # print(arrive_city)
            lowest_price = data['lowest_price']
            # print(lowest_price)
            criteria_token = data['criteria_token']
            # print(criteria_token)
            ##找groupid 的TPE
            # group_location = sql_result_sub['group_key']
            # print(group_location)
            # print(data['id'],start_date)
            timeString = start_date
            struct_time = time.strptime(timeString, "%Y-%m-%d")
            new_timeString = time.strftime("%Y%m%d", struct_time)
            # print(new_timeString)
            sql_sub = "SELECT * FROM skike.flight_price inner JOIN skike.flight_ticket  on flight_ticket.id = flight_price.flight_id where flight_ticket.id = '{}' and flight_ticket.data_query_time='{}' and flight_price.group_id like'%{}%'".format(data['id'],start_date,new_timeString)
            # sql_sub = "SELECT distinct (price) , depart_city, arrive_City, data_query_time, duration_min, depart_time, arrive_time, stopover_minutes, aircraft_registration, stayover_times, flight_company, category FROM skike.flight_ticket INNER JOIN skike.flight_price on flight_ticket.id = flight_price.flight_id where flight_ticket.arrive_City = '{}';".format(location)
            cursor.execute(sql_sub)
            result_sub = cursor.fetchall()
            # print(result_sub)
            flight_id = result_sub[0]['group_id'].split('-')
            flight_id = flight_id[0]
            flight_company_id = flight_id[0:2]
            # get_flight_ticket_alter(start_date, lowest_price, criteria_token ,flight_id,flight_company_id)
            # print("----------------------------------------")
            # result_sub.extend(get_flight_ticket_alter(start_date, lowest_price, criteria_token ,flight_id,flight_company_id))
            # print(result_sub)
            # data['alternative_flight'] = result_sub
            # print(get_flight_ticket_alter(start_date, lowest_price, criteria_token ,flight_id,flight_company_id))
            alternative_flight_list = []
            for ticket in get_flight_ticket_alter(start_date, lowest_price, criteria_token ,flight_id,flight_company_id):
                # print(ticket)
                if int(ticket['available_tickets'])>=int(select_adult):
                    alternative_flight_list.append(ticket)
            # print(alternative_flight_list)
            # data['alternative_flight'] = get_flight_ticket_alter(start_date, lowest_price, criteria_token ,flight_id,flight_company_id)
            data['alternative_flight'] = alternative_flight_list
            # print(data)
            sql_get.append(data)
            # print(sql_get)
            print("----------------------------------------")
        # try:    # print(sql_get)
        #     print(sql_get['alternative_flight'])
        # except Exception as e:
        #     print("Exeception occured:{}".format(e))
        return render_template('skike_flight.html', flight_list=sql_get, today =today, tomorrow= tomorrow,start_date = start_date, location =location,location_arrive =location_arrive,login =login)
    else:
        return redirect(url_for("user_sign_in"))

@app.route('/api/1.0/hotel/<int:id>/<float:geocode_lat>/<float:geocode_lng>/<string:start_date>', methods=['GET','POST'])
def hotel_detail(id, geocode_lat,geocode_lng,start_date):
    email = session.get('email')  # 取session
    if email:
        flash("welcome!")
        login = True
        # return 'welcome %s' % username
    # print(id,geocode_lat,geocode_lng,start_date)
        rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
                            user="admin",password=config.RDSMASTERPASSWORD,\
                            port=3306,database="skike",\
                            cursorclass = pymysql.cursors.DictCursor)
        cursor = rdsDB.cursor()
        print(request.form)
        if request.method == 'POST':
            sql_airport_alter = "SELECT * FROM skike.flight_geocode  where airport_name = '{}';".format(request.form['airport_alter'])
            cursor.execute(sql_airport_alter)
            airport_result = cursor.fetchone()
            near_airport_lat = airport_result['geocode_lat']
            near_airport_lng = airport_result['geocode_lng']
            geo_result = airport_result['airport_name']
            sql_geocode = "SELECT * FROM skike.flight_geocode;"
            cursor.execute(sql_geocode)
            result_sql_geocode = cursor.fetchall()
        elif request != "POST":
            sql_geocode = "SELECT * FROM skike.flight_geocode;"
            cursor.execute(sql_geocode)
            result_sql_geocode = cursor.fetchall()
            geo_result = ""
            geo_number = 999999999999999
            for location in result_sql_geocode:
                euclidean_distance= (location["geocode_lat"]-geocode_lat)**2+(location["geocode_lng"]-geocode_lng)**2
                if euclidean_distance<geo_number:
                    geo_result = location["airport_name"]
                    geo_number = (location["geocode_lat"]-geocode_lat)**2+(location["geocode_lng"]-geocode_lng)**2
                    near_airport_lat =location["geocode_lat"]
                    near_airport_lng =location["geocode_lng"]
                # print(geo_result, geo_number, near_airport_lat, near_airport_lng)

            # sql_get =[]
            # sql_sub = "SELECT * FROM skike.hotel inner join skike.hotel_alternative on hotel.id =hotel_alternative.hotel_id where hotel.id = '{}';".format(str(id))
        sql_agency = "SELECT distinct (hotel_agency) FROM skike.hotel inner join skike.hotel_alternative on hotel.id =hotel_alternative.hotel_id where hotel.id = '{}' order by hotel_alternative.hotel_agency;".format(str(id))
        cursor.execute(sql_agency)
        result_agency = cursor.fetchall()
        # sql_sub = "SELECT * FROM skike.hotel inner join skike.hotel_alternative on hotel.id =hotel_alternative.hotel_id where hotel.id = '{}' order by hotel_alternative.hotel_agency;".format(str(id))
        sql_sub = "SELECT * FROM skike.hotel where id = '{}'".format(str(id))
        cursor.execute(sql_sub)
        result_sub = cursor.fetchall()
        # sql_get.append(data)
        sql_name = result_sub[0:1]
        result_sub_2 = get_hotel_alter(start_date, id)
        # print(result_sub_2['agency'])
        agency_list = result_sub_2['agency']
        num_result_sub_2 = len(result_sub_2['newlist'])
        # print(agency_list)
        result_sub_2 = result_sub_2['newlist']
        # print(start_date, id)
        
        # sql_sub_2 = "SELECT * FROM skike.hotel_alternative where hotel_id = '{}' and data_query_time ='{}' order by hotel_agency asc".format(str(id),start_date)
        # cursor.execute(sql_sub_2)
        # result_sub_2 = cursor.fetchall()
        # print(result_sub_2)
        # sql_get.append(data)
        sql_name = result_sub[0:1]
        url = "https://maps.googleapis.com/maps/api/directions/json?language=zh-TW&origin={},{}&destination={},{}&mode=transit&key={}".format(near_airport_lat,near_airport_lng,geocode_lat,geocode_lng,config.GOOGLE_API_KEY)
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        result = response.json()
        # print(result)
        if result['status'] =='ZERO_RESULTS':
            error_msg = "The direction service is not support for this airport the hotel"
            flash("")
            return redirect(url_for('hotel_detail',id=id, geocode_lat=geocode_lat,geocode_lng=geocode_lng,start_date=start_date,error_msg=error_msg))
        elif result['status'] =='REQUEST_DENIED':
            print('enter api denied')
            return render_template('skike_hotel_detail_origin.html',detail_hotel_list = result_sub_2, result_agency = result_agency, sql_name = sql_name, google_api = config.GOOGLE_API_KEY, agency_list = agency_list ,start_date = start_date,id=id,num_result_sub_2 = num_result_sub_2)
        # with open(r"C:\Users\Ben Fan\Desktop\skike\Main_20211013_project\testmap.json",encoding="utf-8") as f:
        # with open(r"C:\Users\Ben Fan\Desktop\skike\Main_20211013_project\api.json",encoding="utf-8") as f:
        #     result= json.load(f)
            # print(result)
        direction_list =[]
        geo_list = []
        route_flow = []
        print("-----------------------------------------")
        translator = Translator()
        arrival_time = result['routes'][0]['legs'][0]["arrival_time"]["value"]
        departure_time = result['routes'][0]['legs'][0]["departure_time"]["value"]
        go_list=[]
        # print(arrival_time-departure_time)
        date_time = datetime.fromtimestamp(arrival_time)
        date_time_depart = datetime.fromtimestamp(departure_time)
        need_time = int(arrival_time-departure_time)
        need_hour = int(need_time/3600)
        need_min = int((need_time-3600*need_hour)/60)
        # print(1)
        print(need_time)
        d_arrival_time = date_time.strftime("%H:%M:%S")
        date_time_depart = date_time_depart.strftime("%H:%M:%S")
        print(d_arrival_time,date_time_depart)
        for i in range (0, len (result['routes'][0]['legs'][0]['steps'])):
            print(result['routes'][0]['legs'][0]['steps'][i]['travel_mode'])
            if result['routes'][0]['legs'][0]['steps'][i]['travel_mode']=="TRANSIT":
                ta_arrive_time =result['routes'][0]['legs'][0]['steps'][i]['transit_details']['arrival_time']['value']
                ta_depart_time =result['routes'][0]['legs'][0]['steps'][i]['transit_details']['departure_time']['value']
                date_time2 = datetime.fromtimestamp(ta_arrive_time)
                date_time_depart2 = datetime.fromtimestamp(ta_depart_time)
                d_arrival_time2 = date_time2.strftime("%H:%M:%S")
                date_time_depart2 = date_time_depart2.strftime("%H:%M:%S")
                go_list.append(date_time_depart2)
                go_list.append(d_arrival_time2)
                # print(d_arrival_time2,date_time_depart2)
            j = result['routes'][0]['legs'][0]['steps'][i]['html_instructions'] 
            # j = translator.translate(j,src='zh-cn', dest='zh-tw').text
            route_flow.append(j)
            geo_list.append(polyline.decode(result['routes'][0]['legs'][0]['steps'][i]["polyline"]['points']))
        go_list.append(d_arrival_time)
        print("------------------------------------------------------------------------------------")
        # print(go_list)
        # print(route_flow)

        route_flow2 = dict(zip(route_flow, go_list))
        print(route_flow2) 
        # print(geo_list)
        # for item in result['routes'][0:1]:
        #     # print(item['overview_polyline']['points'])
        #     geo_list.append(polyline.decode(item['overview_polyline']['points']))
        #     for item2 in item['legs'][0:1]:
        #         direction_list.append(item2)
        #         # for item3 in item2['steps']:
        #         #     print(item3['polyline']['points']+"\n")
        #             # geo_list.append(polyline.decode(item3['polyline']['points']))
        #             # direction_list.append(item3)
        #                 # try:
        #                 #     print(item3["transit_details"])
        #                 # except Exception as e:
        #                 #     print("Exeception occured:{}".format(e))
        #     print("------------------------------------------------------------------------------------------------")
        # print(direction_list)

        print("_____________________")
        return render_template('skike_hotel_detail_origin.html',detail_hotel_list = result_sub_2, result_agency = result_agency, sql_name = sql_name, google_api = config.GOOGLE_API_KEY,direction_list = direction_list, test_code = geo_list, geocode=result_sql_geocode,geocode_lat = geocode_lat,geocode_lng=geocode_lng,route_flow2 = route_flow2, geo_result = geo_result, today = today, tomorrow = tomorrow,agency_list =agency_list, start_date = start_date,id=id,num_result_sub_2 = num_result_sub_2,start_time = date_time_depart,login =login,need_hour=need_hour,need_min =need_min)
    else:
        return redirect(url_for("user_sign_in"))
        # for i in range (0, len (result['routes'][0]['legs'][0]['steps'])):
        #     j = result['routes'][0]['legs'][0]['steps'][i]['html_instructions'] 
        #     print(j)    

@app.route('/route_function/hotel_detail',methods=[ "GET",'POST'])
def route_function_hotel_detail():
    # print(request.form)
    checkbox = request.form.get('checkbox')
    
    agency_selected = request.form.get('agency_selected')
    start_date = request.form.get('start_date')
    id = request.form.get('id')
    agency_result_1st = request.form.get('agency_result')
    result_feature= checkbox.split('|')
    while '' in result_feature:
        result_feature.remove('')
    feature_dict ={}
    feature_dict['checkbox'] = result_feature
    feature_dict['agency_selected'] = agency_selected
    result_sub_2 = get_hotel_alter(start_date, id,feature_dict =feature_dict, agency_result_1st=agency_result_1st)
    num_result_sub_2 = len(result_sub_2['newlist'])
    result_sub_2['num_result_sub_2']= num_result_sub_2
    try:
        print(123)

    except Exception as e:
        print("Exeception occured:{}".format(e))
    return result_sub_2
@app.route('/api/1.0/bootstrap', methods=['GET'])
def boot():
    return render_template('user_login.html')

# @app.route('/api/1.0/airport_insert', methods=['GET'])
# def airport():
#     rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
#                             user="admin",password=config.RDSMASTERPASSWORD,\
#                             port=3306,database="skike",\
#                             cursorclass = pymysql.cursors.DictCursor)
#     cursor = rdsDB.cursor()
#     add_list = []
#     for dic in config.airport_geo_list_KR:
#         for key,value in dic.items():
#             # print(key,value)
#             add_list.append((key,value[0],value[1]))
#     sql_airport = "INSERT INTO skike.flight_geocode (`airport_name`, `geocode_lat`, `geocode_lng`)VALUES ( %s, %s, %s)"
#     try:
#         cursor.executemany(sql_airport,add_list)
#         rdsDB.commit()
#     except Exception as e:
#         print("Exeception occured:{}".format(e))
#     return "ok"