from collections import defaultdict
from flask import request, render_template, jsonify
import os
import random,datetime,time,json
import pymysql
from server import app
from server.models.product_model import get_products, get_products_variants
from werkzeug.utils import secure_filename
from pymongo import MongoClient
##########
import sys
sys.path[0] += '\\..'
from env import config

PAGE_SIZE = 6
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

@app.route('/')
@app.route('/admin/main.html', methods=['GET'])
def main_index():
    return render_template('skike_main2.html')



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

@app.route('/api/1.0/tickets/tokyo', methods=['get'])
def tokyo():
    paging = request.args.get('paging')
    if paging == None or paging == '':
        paging = 0
    rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
                        user="admin",password=config.RDSMASTERPASSWORD,\
                        port=3306,database="skike",\
                        cursorclass = pymysql.cursors.DictCursor)
    cursor = rdsDB.cursor()
    sql = "SELECT * FROM skike.flight_ticket where data_query_time ='{}' order by data_query_time asc LIMIT {},{}".\
        format('2021-10-24',str(int(paging)*6),6)
    cursor.execute(sql)
    sql_result = cursor.fetchall()
    # sql1 = [data for data in sql_result]
    # print(sql1) 
    sql_get =[]
    for data in sql_result:
        sql_sub = "SELECT distinct (price) FROM skike.flight_ticket INNER JOIN skike.flight_price on flight_ticket.id = flight_price.flight_id where flight_ticket.id = '{}';".format(data['id'])
        cursor.execute(sql_sub)
        result_sub = cursor.fetchall()
        # print([data['price'] for data in result_sub])
        data['alternative_flight'] = result_sub
        # print(result_sub)
        sql_get.append(data)
    return render_template('skike_main2.html', flight_list=sql_get)