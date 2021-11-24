import pymysql.cursors

# Connect to the database
import pymysql,json
from datetime import  datetime,timedelta
from server import db
import random,time
import  requests
import operator
import urllib.parse
from server.env import config
import jwt
def connect_db(host, user, password, db_name=None, port=3306):
    try:
        connect_db = pymysql.connect(host=host,
                                     port=port,
                                     user=user,
                                     password=password,
                                     database=db_name,)
        return connect_db
    except pymysql.MySQLError as e:
        print('Got error {!r}, errno is {}'.format(e, e.args[0]))
        return None

def create_db(cursor, DBNAME):
    # create database
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8mb4' ".format(DBNAME)
        )
    except Exception as e:
        print("Exeception occured:{}".format(e))

    # use database
    try:
        cursor.execute("USE {}".format(DBNAME))
    except Exception as e:
        print("Exeception occured:{}".format(e))

    return cursor

def create_tb_flight_ticket(cursor, TABLES, TBNAME=None):
    TABLES[TBNAME] = ("CREATE TABLE IF NOT EXISTS {}( \
        `id` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `criteria_token` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `lowest_price` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `depart_city` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `arrive_City` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `data_query_time` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `duration_min` INT(10) COLLATE utf8mb4_bin NOT NULL, \
        `depart_time` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `arrive_time` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `stopover_minutes` INT(10) COLLATE utf8mb4_bin NOT NULL, \
        `aircraft_registration` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `stayover_times` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `flight_company` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `category` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        PRIMARY KEY (`id`) \
        )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;".format(TBNAME))


def create_tb_stopover(cursor, TABLES, TBNAME=None):
    TABLES[TBNAME] = ("CREATE TABLE IF NOT EXISTS {}( \
        `id` INT(10) COLLATE utf8mb4_bin NOT NULL AUTO_INCREMENT, \
        `terminal_arrive_time` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `flight_depart_terminal` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `flight_arrive_terminal` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `flight_id` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        PRIMARY KEY (`id`), \
        FOREIGN KEY (`flight_id`) REFERENCES flight_ticket(id) \
        )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;".format(TBNAME))

def create_tb_flightprice(cursor, TABLES, TBNAME=None):
    TABLES[TBNAME] = ("CREATE TABLE IF NOT EXISTS {}( \
        `id` INT(10) COLLATE utf8mb4_bin NOT NULL AUTO_INCREMENT, \
        `group_id` Text COLLATE utf8mb4_bin NOT NULL, \
        `price` INT(10) COLLATE utf8mb4_bin NOT NULL, \
        `adult_price` varchar(200) COLLATE utf8mb4_bin NULL, \
        `child_price` varchar(200) COLLATE utf8mb4_bin NULL, \
        `flight_class` varchar(200) COLLATE utf8mb4_bin NOT NULL, \
        `available_tickets` INT(10) COLLATE utf8mb4_bin NOT NULL, \
        `flight_ticket_feature` varchar(200) COLLATE utf8mb4_bin NOT NULL, \
        `flight_category` varchar(200) COLLATE utf8mb4_bin NOT NULL, \
        `ticket_description` varchar(200) COLLATE utf8mb4_bin NOT NULL, \
        `flight_id` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `url` TEXT  COLLATE utf8mb4_bin NOT NULL, \
        PRIMARY KEY (`id`), \
        FOREIGN KEY (`flight_id`) REFERENCES flight_ticket(id) \
        )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;".format(TBNAME))

# def create_tb_flightpriceChild(cursor, TABLES, TBNAME=None):
#     TABLES[TBNAME] = ("CREATE TABLE IF NOT EXISTS {}( \
#         `id` INT(10) COLLATE utf8mb4_bin NOT NULL AUTO_INCREMENT, \
#         `productFlag` INT(10) COLLATE utf8mb4_bin NOT NULL, \
#         `viewTotalPrice` INT(10) COLLATE utf8mb4_bin NOT NULL, \
#         `childPrice` varchar(200) COLLATE utf8mb4_bin NOT NULL, \
#         `productClass` varchar(200) COLLATE utf8mb4_bin NOT NULL, \
#         `availableTickets` INT(10) COLLATE utf8mb4_bin NOT NULL, \
#         `productName` varchar(200) COLLATE utf8mb4_bin NOT NULL, \
#         `productCategory` varchar(200) COLLATE utf8mb4_bin NOT NULL, \
#         `ticketDescription` varchar(200) COLLATE utf8mb4_bin NOT NULL, \
#         `product_id` INT(10) COLLATE utf8mb4_bin NOT NULL, \
#         PRIMARY KEY (`id`), \
#         FOREIGN KEY (`product_id`) REFERENCES flyticket(id) \
#         )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;".format(TBNAME))

def create_tb_airport_geocode(cursor, TABLES, TBNAME=None):
    TABLES[TBNAME] = ("CREATE TABLE IF NOT EXISTS {}( \
        `airport_name` varchar(200) COLLATE utf8mb4_bin NOT NULL, \
        `geocode_lat` float(10) COLLATE utf8mb4_bin NOT NULL, \
        `geocode_lng` float(10) COLLATE utf8mb4_bin NOT NULL, \
        PRIMARY KEY (`airport_name`) \
        )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;".format(TBNAME))

def create_tb_hotel(cursor, TABLES, TBNAME=None):
    TABLES[TBNAME] = ("CREATE TABLE IF NOT EXISTS {}( \
        `id` INT(10) COLLATE utf8mb4_bin NOT NULL, \
        `data_query_time` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `name` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `hotel_near_location` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `hotel_near_location_meter` INT(10) COLLATE utf8mb4_bin NOT NULL, \
        `hotel_rating_count` INT(10) COLLATE utf8mb4_bin NOT NULL, \
        `hotel_rating_avg_score` float(10) COLLATE utf8mb4_bin NOT NULL, \
        `hotel_best_price_per_stay` INT(10) COLLATE utf8mb4_bin NOT NULL, \
        `category` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `locality` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `image_url` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `geocode_lat` float(10) COLLATE utf8mb4_bin NOT NULL, \
        `geocode_lng` float(10) COLLATE utf8mb4_bin NOT NULL, \
        PRIMARY KEY (`id`, `data_query_time`) \
        )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;".format(TBNAME))

def create_tb_user(cursor, TABLES, TBNAME=None):
    TABLES[TBNAME] = ("CREATE TABLE IF NOT EXISTS {}( \
        `email` varchar(255) NOT NULL,\
        `id` int NOT NULL AUTO_INCREMENT,\
        `provider` varchar(15) NOT NULL,\
        `password` varchar(255) NOT NULL,\
        `name` varchar(127) NOT NULL,\
        `picture` varchar(255) DEFAULT NULL,\
        `access_token` text NOT NULL,\
        `access_expired` bigint NOT NULL,\
        `login_at` timestamp NULL DEFAULT NULL,\
        PRIMARY KEY (`id`,`email`,`password`)\
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;".format(TBNAME))

def create_tb_user_favorite(cursor, TABLES, TBNAME=None):
    TABLES[TBNAME] = ("CREATE TABLE IF NOT EXISTS {}( \
        `id` int NOT NULL AUTO_INCREMENT,\
        `email` varchar(255) NOT NULL,\
        `want_time_start` varchar(255) DEFAULT NULL,\
        `want_time_end` varchar(255) DEFAULT NULL,\
        `hotel_name` varchar(255) DEFAULT NULL,\
        `hotel_img` varchar(255) DEFAULT NULL,\
        `hotel_detail` varchar(255) DEFAULT NULL,\
        `name` varchar(127) NOT NULL,\
        `location` varchar(255) DEFAULT NULL,\
        `price` int(10) DEFAULT NULL,\
        PRIMARY KEY (`id`,`email`)\
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;".format(TBNAME))

def create_tb_hotel_alter(cursor, TABLES, TBNAME=None):
    TABLES[TBNAME] = ("CREATE TABLE IF NOT EXISTS {}( \
        `id` INT(10) COLLATE utf8mb4_bin NOT NULL AUTO_INCREMENT, \
        `data_query_time` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `hotel_agency` varchar(255) COLLATE utf8mb4_bin NOT NULL,    \
        `agency_logo` varchar(255) COLLATE utf8mb4_bin NOT NULL,    \
        `hotel_feature` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `price` INT(10) COLLATE utf8mb4_bin NOT NULL, \
        `hotel_url` Text COLLATE utf8mb4_bin  NULL, \
        `hotel_id` INT(10) COLLATE utf8mb4_bin NOT NULL, \
        PRIMARY KEY (`id`,`hotel_feature`,`price`), \
        FOREIGN KEY (`hotel_id`,`data_query_time`) REFERENCES hotel(`id`,`data_query_time`) \
        )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;".format(TBNAME))
    
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
            print("OK")
        except Exception as e:
            print("Exeception occured:{}".format(e))

def get_products(page_size, paging, requirement = {}):
    pass


def get_products_variants(product_ids):
    pass

def get_hotel_alter(data_query_time, hotel_id,feature_dict=None,agency_result_1st=None):
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
    date_1 = datetime.strptime(data_query_time, "%Y-%m-%d")
    item_add_1 = date_1+ timedelta(days =1)
    item_add_1 = item_add_1.date()
    try:
        payload = json.dumps({
        "operationName": "getAccommodationDeals",
        "variables": {
            "accommodationDealsParams": {
            "accommodationNsid": {
                "id": int(hotel_id),
                "ns": 100
            },
            "stayPeriod": {
                "arrival": "{}".format(str(data_query_time)),
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
        if result['data']['getAccommodationDeals']['deals']:
            print("ok")
        else:
            print("re-do")
            time.sleep(2)
            response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
            result = response.json()
        print("data_query_time "+str(data_query_time)+" "+"  ip is "+str(ip))
        # mycollection.insert_one(result)
        # print(result)
        data_list_hotel_detail = []
        data_list_dict ={}
        ##修改取得的價格數量 list 至 10價格
        list_agency=[]
        for hotel_product_detail in result['data']['getAccommodationDeals']['deals']:
            data_list_dict ={}
            try:
                data_query_time = data_query_time
                data_list_dict['data_query_time'] = data_query_time
                if feature_dict and feature_dict['agency_selected']!="全選":
                    if feature_dict['agency_selected'] != hotel_product_detail['advertiser']['name']:
                        continue
                # elif feature_dict==None or(feature_dict and feature_dict['agency_selected'] == hotel_product_detail['advertiser']['name']):
                #     hotel_agency = hotel_product_detail['advertiser']['name']
                hotel_agency = hotel_product_detail['advertiser']['name']
                list_agency.append(hotel_agency)
                data_list_dict['hotel_agency'] = hotel_agency
                agency_logo = "https:"+str(hotel_product_detail['advertiser']['advertiserLogo']['url'])
                data_list_dict['agency_logo'] = agency_logo
                hotel_feature =""
                for features in hotel_product_detail['priceAttributes']:
                    if features["label"] != None and feature_dict==None:
                        hotel_feature+=features["label"]+", "
                hotel_feature+= hotel_product_detail['description']
                if feature_dict!=None:
                    for item in feature_dict['checkbox']:
                        if item in hotel_feature:
                            print(item,hotel_feature)
                            print(item in hotel_feature)
                            break
                data_list_dict['hotel_feature'] = hotel_feature
                price = hotel_product_detail['price']
                data_list_dict['price'] = price
                hotel_url = "https://www.trivago.com.tw"+str(hotel_product_detail['clickoutPath'])
                data_list_dict['hotel_url'] = hotel_url
                hotel_id = hotel_id
                data_list_dict['hotel_id'] = hotel_id

                # data_list_hotel_detail.append((data_query_time,hotel_agency, agency_logo, hotel_feature, price, hotel_url, hotel_id))
                data_list_hotel_detail.append(data_list_dict)            
            except Exception as e:
                print("Exeception occured:{}".format(e))
    except Exception as e:
            print("ERROR:", url, e)
    agency_result = set(list_agency)
    agency_result = sorted(agency_result)
    # print(agency_result)
    newlist = sorted(data_list_hotel_detail, key= operator.itemgetter('hotel_agency'))
    # return data_list_hotel_detail
    if agency_result_1st:
        agency_result = agency_result_1st
    return {'agency':agency_result,'newlist':newlist}


# def get_flight_ticket_alter(dCity,aCity,data_query_time, low_price, criteria_token,flight_no,airlineCode):
def get_flight_ticket_alter(data_query_time, low_price, criteria_token,flight_no,airlineCode):
    url = "https://hk.trip.com/flights/graphql/intlFlightMoreGradeSearch"
    payload = json.dumps({
    "operationName": "intlFlightMoreGradeSearch",
    "variables": {
        "request": {
        "Head": {
            "Currency": "TWD"
        },
        "criteriaToken": "{}".format(criteria_token),
        "lowPrice": int(low_price),
        "origDestRequestInfoList": [
            {
            "segmentNo": 1,
            "flightNo": str(flight_no),
            "departureDate": str(data_query_time),
            "airlineCode": str(airlineCode)
            }
        ]
        }
    },
    "extensions": {
        "persistedQuery": {
        "version": 1,
        "sha256Hash": "b44346ceeb42be5ea900ba8ac033d12c1d69b5161bbce73c90907fdbb195acfa"
        }
    }
    })
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'referer': 'https://hk.trip.com/hotels/home',
    'cookie': 'cookiePricesDisplayed=TWD; _abtest_userid=c9a403a4-5a35-4ac9-b77e-cda4d88ab996; _gcl_au=1.1.22915204.1634111486; _RSG=kVaUkRhJm2DYFZYojM.Dl8; _RGUID=d0b04eb6-ee7a-47ee-8bcd-f96b728a33e2; _RDG=28bff0fb631abf2dcb1bb119dc6b6dfdc5; ibulocale=zh_hk; _gid=GA1.2.449869172.1634461177; ibu_online_permission_cls_ct=2; ibu_online_permission_cls_gap=1634461178358; IBU_TRANCE_LOG_P=18095419643; IBU_TRANCE_LOG_URL=%2Fhotels%2F; g_state={"i_p":1634548318536,"i_l":2}; cticket=54B8FA2D6995EF0A6A2C871BFCDFE940FD844ABA8FECF942FBC70FAF15930247; ticket_ctrip=bJ9RlCHVwlu1ZjyusRi+ypZ7X2r4+yojQBs5yAteRtJUPMMNOT+SyRpl0pXF5gepAwGHqGujQMZNqu5Np9RRpATD41ZlnhnbAbsjedVc3eKnceYddsVGVumT0zU9Bnivj6BAEPDEIzNRpEGOMN4Hu+MYNlHbby12UHiGvm7YBBvHa6Gv02d8ycPSh5rouc5NqvuPoKhR/wq/X8mU+KhF8QRf+0WyGmPyoc+i/T5BhBgEKcZnLYx+zyBL3/dEcpRyQ6nkk0gQH4+YZlwIb7tckbJsGo/Hp3LPfDiaUziecR8=; DUID=u=25F7AAE4752EAC34609CD6D155357263&v=0; IsNonUser=T; ibu_h5_isquick=1; _combined=transactionId%3D3dd51fde-d03d-42b7-9e03-4ea485778639%26usedistributionchannels%3DTrue%26channel%3DTWSite%26uuid%3D66b1b131-266b-4591-9f74-fe4cce2f705b; Union=AllianceID=18500&SID=446383&OUID=5968_1588917737_20677554da3d837022edc664fd0fa817&SourceID=&AppID=&OpenID=&Expires=1637128277741&createtime=1634536277; ibulanguage=HK; carsearch=residency%3D1%26age%3D30; OsdSessionId=5a2150ae5d534fd8bd4d80e2ae9abc0d; _tp_search_latest_channel_name=hotels; librauuid=Q7AMCkfGHo0aCbmO; IBU_showtotalamt=0; intl_ht1=h4%3D219_48903776%2C219_6112682; hotel=48903776; ibu_online_home_language_match={"isFromTWNotZh":false,"isFromIPRedirect":false,"isFromLastVisited":false,"isRedirect":false,"isShowSuggestion":false,"lastVisited":"https://hk.trip.com?locale=zh-hk"}; _RF1=1.200.7.185; _uetsid=a75bd1402f2811ecacca45fdcb9c1c7c; _uetvid=ecbdcf902cb511eca0e9a92191716a1b; _ga_X437DZ73MR=GS1.1.1634547264.13.1.1634547308.0; _bfa=1.1634111485004.3fwpku.1.1634545222673.1634547264357.13.438; _bfs=1.2; _ga=GA1.2.1003449919.1634111485; _bfi=p1%3D10320668150%26p2%3D10320668150%26v1%3D438%26v2%3D437; cookiePricesDisplayed=TWD; ibulanguage=HK; ibulocale=zh_hk',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    result = response.json()
    # print(result)
    # print(result)
    alter_list = []
    if result['data']['intlFlightMoreGradeSearch']['productInfo']:
        data = result['data']['intlFlightMoreGradeSearch']['productInfo']
        for product in data['policyInfoList']:
            alter_dict = {}
            #criteriaToken,remark_token_key,shoppingId,groupKey
            #criteriaToken相同;remarkTokenKey ,shoppingid,groupkey不同
            try:
                remark_token_key = product["remarkTokenKey"]
                main_class = product["mainClass"]
                available_tickets = product["availableTickets"]
                promise_minutes = product['ticketDeadlineInfo']['promiseMinutes']
                price = product["priceDetailInfo"]["viewTotalPrice"]
                group_key = product["productKeyInfo"]["groupKey"]
                shopping_id = product["productKeyInfo"]["shoppingId"]
                description = product["descriptionInfo"]['productName']+product["descriptionInfo"]['ticketDescription']
                url = "https://hk.trip.com/flights/passenger?FlightWay=OW&class=Y&Quantity=1&ChildQty=0&BabyQty=0&dcity=&acity=&ddate=&"
                remark_token_key = urllib.parse.quote_plus(remark_token_key)
                criteriaToken = urllib.parse.quote_plus(criteria_token)
                shoppingId = urllib.parse.quote_plus(shopping_id)
                groupKey = urllib.parse.quote_plus(group_key)
                a = "remarkTokenKey="+remark_token_key+"&"+"criteriaToken="+criteriaToken+"&"+"shoppingId="+shoppingId+"&"+"groupKey="+groupKey
                url+=a
                ###現在用到組url的部分
                flight_class = product['productClass'][0]
                alter_dict['remark_token_key']= remark_token_key
                alter_dict['main_class']= main_class
                alter_dict['available_tickets']= available_tickets
                alter_dict['promise_minutes']= promise_minutes
                alter_dict['price']= price
                alter_dict['group_key']= group_key
                alter_dict['shopping_id']= shopping_id
                alter_dict['description']= description
                alter_dict['url']= url
                alter_dict['flight_class']= flight_class
                alter_list.append(alter_dict)
                # print(alter_list)
            except Exception as e:
                print("Exeception occured:{}".format(e))
        # return alter_flight_list
        return alter_list
    else:
        return alter_list


def get_hotel_more_pic(hotel_id, want_time_start, want_time_end):
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
    try:
        url = "https://www.trivago.com.tw/graphql"
        payload = json.dumps({
        "operationName": "getGallery",
        "variables": {
            "input": {
            "nsids": [
                {
                "id": int(hotel_id),
                "ns": 100
                }
            ]
            },
            "pagination": {
            "limit": 30
            },
            "shouldGetAdvertiserLinks": False,
            "advertiserLinksInput": {
            "linkType": "IMAGE",
            "stayPeriod": {
                "arrival": "{}".format(want_time_start),
                "departure": "{}".format(want_time_end)
            },
            "rooms": [
                {
                "adults": 1,
                "children": []
                }
            ]
            }
        },
        "extensions": {
            "persistedQuery": {
            "version": 1,
            "sha256Hash": "92e168f0849d34d063e0a69a3f3e8e7680d4f62c783a1add689814855967c5a2"
            }
        }
        })
        headers = {
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
        'apollographql-client-version': 'v93_10_5_ae_f07e1e495a0',
        'Cookie': 'ak_bmsc=2F85A1AEDFDAF2358CE695956720FCB1~000000000000000000000000000000~YAAQhz7cPfZmFyx9AQAAFS15Sw1px02olyRVYUKlW9tZMyMjRwZiQBdJ1IwBWL1Aw+05iMMUhQyxnBOv7pMrihNjEg0qSKt5k7L/nr7z115Fx4qpCHWyIThEyHbya68co7fYYb4gDp0V3RHb/1t8W3LAVeHyMatFs2NUcO3DSH+zmcW1ifDMU0RR0ORMNj8a8LE3Ev+mhAQP5dy+ipXy7uwt9KDQ/EtiArq57gfemsIzofQON2j4Yv8WBpP4Q/Jh9tCg0TcikYZ3lKaHd2vKNIqxXiQHdiZzMbw3GAdqPjn+/v4g09khMeExxKhxNEwCr3vrd6CNkA7cobBWDQmxa287wYomDUvtUJCs4c+pkQOBCqcOdhAme5SNG448OArW; edge_tid=0882dd417534e3d783b2d8155d; edge_tid_s=0882dd417534e3d783b2d8155d'
        }
        ip = random.choice(m)
        proxies = {'http':"http://{}:{}@{}".format('vvbocpqj','obt7b7ug0dim',ip)}
        response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
        result = response.json()
        img_url=[]
        if result['data']['getAccommodationDetails']['accommodationDetails']:
            print("ok")
        else:
            print("re-do")
            time.sleep(2)
            response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
            result = response.json()
        gallery = result['data']['getAccommodationDetails']['accommodationDetails'][0]['gallery']['images']
        for images in gallery:
            # print("https://imgcy.trivago.com/d_dummy.jpeg,f_auto,q_auto/if_iw_lte_ih,c_scale,w_236/if_else,c_scale,h_160/e_improve,q_auto:low/{}.jpeg".format(images['urlTail']))
            img_url.append(("https://imgcy.trivago.com/d_dummy.jpeg,f_auto,q_auto/if_iw_lte_ih,c_scale,w_236/if_else,c_scale,h_160/e_improve,q_auto:low/{}.jpeg".format(images['urlTail'])))
    except Exception as e:
        print("Exeception occured:{}".format(e))
    return img_url

def check_exist_user(rdsDB,email):
    rdsDB = rdsDB
    print(rdsDB)
    cursor = rdsDB.cursor()
    query = 'SELECT * FROM skike.user where email = "{}";'.format(str(email))
    cursor.execute(query)
    sign_up_data = cursor.fetchone()
    print
    rdsDB.commit()
    rdsDB.close()
    return sign_up_data

def insert_register_data(rdsDB,provider, name, email,hashed_password, picture,acceess_expire):
    tokenSignUp = jwt.encode({'provider':provider,\
                                  'name':name,\
                                  'email': email }, config.SECRET_KEY)
    try:
        sign_up_data = "INSERT INTO `user` (`provider`, `name`,\
                                    `email`, `password`, `picture`,\
                                    `access_token`, `access_expired`) \
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor = rdsDB.cursor()
        cursor.execute(sign_up_data, (provider, name, email,\
                                    hashed_password, picture, tokenSignUp,\
                                    acceess_expire))
        rdsDB.commit()
    except Exception as e:
        print("Exeception occured:{}".format(e))
    rdsDB.close()


def insert_signin_data(rdsDB,email):
    try:
        cursor = rdsDB.cursor()
        query = 'SELECT * FROM skike.user WHERE email = "{}" ;'.format(email)
        cursor.execute(query)
        sign_data = cursor.fetchone()
        print(sign_data)
        rdsDB.commit()
    except Exception as e:
        print("Exeception occured:{}".format(e))
    return sign_data

def get_hotel_search_list(rdsDB,start_date,end_date,location):
    cursor = rdsDB.cursor()
    sql = "SELECT * FROM skike.hotel where DATE(hotel.data_query_time) BETWEEN '{}' AND '{}' group by name having locality like'{}' order by hotel_rating_count desc limit 1000".format(start_date,end_date,location)
    cursor.execute(sql)
    sql_result = cursor.fetchall()
    return sql_result
def get_hotel_search_coount(rdsDB,start_date,end_date,location):
    cursor = rdsDB.cursor()
    sql_count = "SELECT count(distinct(name)) FROM skike.hotel where DATE(hotel.data_query_time) BETWEEN '{}' AND '{}' AND locality ='{}' group by name;".format(start_date,end_date,location)
    cursor.execute(sql_count)
    sql_count_result = cursor.fetchall()
    return sql_count_result
def get_user_page_data(conn,email):
    mydatabase = conn['skike_origin']
    mycollection=mydatabase['skike_favorite']
    pipeline=[
    {
        '$match': {
            'email': '{}'.format(email)
        }
    }
    ]
    result =mycollection.aggregate(pipeline)
    results = [doc for doc in result]
    return results

def get_hotel_search(rdsDB,start_date,end_date,location):
    cursor = rdsDB.cursor()
    sql = "SELECT * FROM skike.hotel where DATE(hotel.data_query_time) BETWEEN '{}' AND '{}' group by name having locality like'{}' order by hotel_rating_count desc limit 1000".format(start_date,end_date,location)
    cursor.execute(sql)
    sql_result = cursor.fetchall()
    return sql_result

def get_hotel_search_number(rdsDB,start_date,end_date,location):
    cursor = rdsDB.cursor()
    sql_count = "SELECT count(distinct(name)) FROM skike.hotel where DATE(hotel.data_query_time) BETWEEN '{}' AND '{}' AND locality ='{}' group by name;".format(start_date,end_date,location)
    cursor.execute(sql_count)
    sql_count_result = cursor.fetchall()
    return sql_count_result

def delete_user_favorite_item(conn, email, hotel_name=None, hotel_detail=None, hotel_img=None):
    mydatabase = conn['skike_origin']
    mycollection=mydatabase['skike_favorite']
    if email and hotel_name:
        myquery = {"email":email,"hotel_name":hotel_name}
    elif email and hotel_detail and hotel_img:
        myquery = {"email":email,"hotel_detail":hotel_detail,"hotel_img":hotel_img}
    mycollection.remove(myquery)

def add_user_favorite_item(conn, email, want_time_start, want_time_end, hotel_name,hotel_img,hotel_detail,user_name,location,price):
    mydatabase = conn['skike_origin']
    mycollection=mydatabase['skike_favorite']
    result = {"email":email, "want_time_start":want_time_start, "want_time_end":want_time_end, "hotel_name":hotel_name, "hotel_img":hotel_img, "hotel_detail":hotel_detail, "name":user_name,"location":location,"price":price}
    mycollection.insert_one(result)

def get_re_sort_result(rdsDB, start_date,end_date,location,condition1,condition2):
    cursor = rdsDB.cursor()
    sql = "SELECT * FROM skike.hotel where DATE(hotel.data_query_time) BETWEEN '{}' AND '{}' group by name having locality like'{}' order by {} {} limit 1000".format(start_date,end_date,location,condition1,condition2)
    cursor.execute(sql)
    sql_result = cursor.fetchall()
    return sql_result

def get_flight_ticket_plan(rdsDB,start_date,location_arrive,location):
    cursor = rdsDB.cursor()
    sql = "SELECT * FROM skike.flight_ticket where data_query_time ='{}' and  arrive_City = '{}' and depart_city ='{}';".format(start_date,location_arrive,location)
    cursor.execute(sql)
    sql_result = cursor.fetchall()
    return sql_result

# def add_flight_pic_url(sql_result):
#     for sql_result_sub in sql_result:
#         air_pic = sql_result_sub['flight_company'].split(' ')
#         air_pic = air_pic[1]
#         air_pic = air_pic[0:2]
#         air_pic = "https://pic.tripcdn.com/airline_logo/3x/{}.webp".format(air_pic.lower())
#         sql_result_sub['air_pic'] = air_pic

def get_moregrade_price(rdsDB,sql_get,sql_result,start_date,select_adult):
    cursor = rdsDB.cursor()
    for data in sql_result:
        air_pic = data['flight_company'].split(' ')
        air_pic = air_pic[1]
        air_pic = air_pic[0:2]
        air_pic = "https://pic.tripcdn.com/airline_logo/3x/{}.webp".format(air_pic.lower())
        data['air_pic'] = air_pic
        depart_city = data['depart_city'].split(',')
        depart_city = depart_city[1]
        arrive_city = data['arrive_City'].split(',')
        arrive_city = arrive_city[1]
        lowest_price = data['lowest_price']
        criteria_token = data['criteria_token']
        timeString = start_date
        struct_time = time.strptime(timeString, "%Y-%m-%d")
        new_timeString = time.strftime("%Y%m%d", struct_time)
        sql_sub = "SELECT * FROM skike.flight_price inner JOIN skike.flight_ticket  on flight_ticket.id = flight_price.flight_id where flight_ticket.id = '{}' and flight_ticket.data_query_time='{}' and flight_price.group_id like'%{}%'".format(data['id'],start_date,new_timeString)
        cursor.execute(sql_sub)
        result_sub = cursor.fetchall()
        flight_id = result_sub[0]['group_id'].split('-')
        flight_id = flight_id[0]
        flight_company_id = flight_id[0:2]
        alternative_flight_list = []
        for ticket in get_flight_ticket_alter(start_date, lowest_price, criteria_token ,flight_id,flight_company_id):
            if int(ticket['available_tickets'])>=int(select_adult):
                alternative_flight_list.append(ticket)
        data['alternative_flight'] = alternative_flight_list
        sql_get.append(data)

def get_nearest_airport(rdsDB,airport_alter):
    sql_airport_alter = "SELECT * FROM skike.flight_geocode  where airport_name = '{}';".format(airport_alter)
    cursor = rdsDB.cursor()
    cursor.execute(sql_airport_alter)
    airport_result = cursor.fetchone()
    near_airport_lat = airport_result['geocode_lat']
    near_airport_lng = airport_result['geocode_lng']
    geo_result = airport_result['airport_name']
    sql_geocode = "SELECT * FROM skike.flight_geocode;"
    cursor.execute(sql_geocode)
    result_sql_geocode = cursor.fetchall()
    return {"near_airport_lat":near_airport_lat,"near_airport_lng":near_airport_lng,"geo_result":geo_result,"result_sql_geocode":result_sql_geocode}

def get_airport_list(rdsDB,geocode_lat,geocode_lng,MAX_NUMBER):
    cursor = rdsDB.cursor()
    sql_geocode = "SELECT * FROM skike.flight_geocode;"
    cursor.execute(sql_geocode)
    result_sql_geocode = cursor.fetchall()
    geo_result = ""
    geo_number = MAX_NUMBER
    for location in result_sql_geocode:
        euclidean_distance= (location["geocode_lat"]-geocode_lat)**2+(location["geocode_lng"]-geocode_lng)**2
        if euclidean_distance<geo_number:
            geo_result = location["airport_name"]
            geo_number = (location["geocode_lat"]-geocode_lat)**2+(location["geocode_lng"]-geocode_lng)**2
            near_airport_lat =location["geocode_lat"]
            near_airport_lng =location["geocode_lng"]
    return {"geo_result":geo_result,"near_airport_lat":near_airport_lat,"near_airport_lng":near_airport_lng}

def get_hotel_detail_by_id(rdsDB,id):
    cursor = rdsDB.cursor()
    sql_sub = "SELECT * FROM skike.hotel where id = '{}'".format(str(id))
    cursor.execute(sql_sub)
    result_sub = cursor.fetchall()