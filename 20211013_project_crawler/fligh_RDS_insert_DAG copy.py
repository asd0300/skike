from datetime import timedelta


import pymysql
from pymongo import MongoClient
###date generator
from datetime import date, timedelta
from env import config


def flight_data_insert():
    rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
                            user="admin",password=config.RDSMASTERPASSWORD,\
                            port=3306,database="skike",\
                            cursorclass = pymysql.cursors.DictCursor)
    cursor = rdsDB.cursor()
    conn = MongoClient("mongodb://skike4:Asd7788123@ec2-18-191-175-148.us-east-2.compute.amazonaws.com:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false")
    mydatabase = conn['skike'] 
    mycollection=mydatabase['({})skike_ticket_to_JP'.format(str(date.today()))]
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
            total_price = product['policyInfoList'][0]['priceDetailInfo']['viewTotalPrice']
            policy_info_list = product['policyInfoList']
        
            for item in flight_info_list:
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
            # try:                    
            #     cursor.execute(sql_flyticket, (id, depart_city, arrive_City, data_query_time, duration_min, depart_time, arrive_time, stopover_minutes, aircraft_registration, stayover_times, flight_company, category))
            #     rdsDB.commit()
            # except Exception as e:
            #     print("Exeception occured:{}".format(e))

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
                # try:                    
                #     cursor.execute(sql_stopover, (terminal_arrive_time, flight_depart_terminal, flight_arrive_terminal, shoppingId))
                #     rdsDB.commit()
                # except Exception as e:
                #     print("Exeception occured:{}".format(e))
            
            if product['policyInfoList'][0]['priceDetailInfo']['adult'] != None:
                for policy_item in policy_info_list:
                    product_flag =  policy_item['productFlag'],
                    price = policy_item['priceDetailInfo']['viewTotalPrice'],
                    adult_price = str(policy_item['priceDetailInfo']['adult']['totalPrice']),
                    flight_class = str(policy_item['productClass'][0]),
                    available_tickets = policy_item['availableTickets'],
                    flight_ticket_feature = str(policy_item['descriptionInfo']['productName']),
                    flight_category = str(policy_item['descriptionInfo']['productCategory']),
                    ticket_description = str(policy_item['descriptionInfo']['ticketDescription']),
                    flight_id = shoppingId

                    sql_flightprice = "INSERT INTO skike.flight_price (`product_flag`, `price`, `adult_price`, `flight_class`, `available_tickets`, `flight_ticket_feature`, `flight_category`, `ticket_description`, `flight_id`\
                    )VALUES (%s,  %s, %s, %s, %s, %s, %s, %s, %s)"
                    # try:                    
                    #     cursor.execute(sql_flightprice, (product_flag, price, adult_price,  flight_class, available_tickets, flight_ticket_feature, flight_category, ticket_description, flight_id))
                    #     rdsDB.commit()
                    # except Exception as e:
                    #     print("Exeception occured:{}".format(e))

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
                    # try:                    
                    #     cursor.execute(sql_flightpriceChild, (product_Flag, view_total_price, child_price, product_class, available_tickets, product_name, product_category, ticket_description, shoppingId))
                    #     rdsDB.commit()
                    # except Exception as e:
                    #     print("Exeception occured:{}".format(e))
    return "Ok"

flight_data_insert()