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
from server.models.product_model import get_hotel_alter,check_exist_user,insert_register_data,insert_signin_data,get_hotel_search_list,get_hotel_search_coount,get_user_page_data,get_hotel_search,get_hotel_search_number,delete_user_favorite_item,add_user_favorite_item,get_re_sort_result,get_flight_ticket_plan,get_moregrade_price,get_nearest_airport,get_airport_list
from server.env import config
from itertools import count
import polyline
from googletrans import Translator
import bcrypt
import redis
from flask_session import Session

app.secret_key = config.SECRET_KEY
SECRET_KEY = config.SECRET_KEY
# sys.path[0] += '\\..'
from ..env import config
app.config['SESSION_COOKIE_SECURE'] = True

ACCESS_EXPIRE = 86400
MAX_NUMBER = 999999999999999
HOUR_IN_SECOND = 3600
MINUTE_IN_SECOND = 60
PAGE_SIZE = 6
rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
            user="admin",password=config.RDSMASTERPASSWORD,\
            port=config.RDSPORT,database="skike",\
            cursorclass = pymysql.cursors.DictCursor)

conn = MongoClient("mongodb://{}:{}@ec2-18-223-232-121.us-east-2.compute.amazonaws.com:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false".format(config.MONGO_PASS_SKIKE_SKIKE_ORIGIN_ACCOUNT,config.MONGO_PASS_SKIKE_SKIKE_ORIGIN_PASS))

KR_location_list = [k for k,v in config.locLN_KR.items()]
today = str(date.today())
tomorrow = str(date.today()+timedelta(days=1))
next_week = str(date.today()+timedelta(days=7))
# f_session = Session()

# app.config['SECRET_KEY'] = config.SECRET_KEY
# app.config['SESSION_USE_SIGNER'] = True 
# app.config['SESSION_TYPE'] = 'redis'
# app.config['SESSION_KEY_PREFIX'] = 'session:'
# app.config['PERMANENT_SESSION_LIFETIME'] = 7200 
# app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port='6379', db=4)
# f_session.init_app(app)

def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password.encode('utf8'), bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf8'), hashed_password.encode('utf8'))

@app.route('/')
@app.route('/admin/main_flight', methods=['GET'])
def main_index():
    email = session.get('email')  # 取session
    if email:
        login = True
        return render_template('main.html',KR_location_list = KR_location_list,today = today, tomorrow = tomorrow, login =login)
        # return 'welcome %s' % username
    else:
        return render_template('main.html',KR_location_list = KR_location_list,today = today, tomorrow = tomorrow)

@app.route('/sign_out')
def sign_out():
    try:
        session.pop('email')
    except Exception as e:
                    print("Exeception occured:{}".format(e))
    return redirect(url_for('main_index'))

@app.route('/admin/user_page/', methods=['GET'])
def user_page():
    email = session.get('email')  # 取session
    if email:
        login = True
        results = get_user_page_data(conn,email)
        return render_template('user_page.html',KR_location_list = KR_location_list,today = today, tomorrow = tomorrow, login =login,sql_favorite_result_hotel=results,email=email)
    else:
        return redirect(url_for("user_sign_in"))

@app.route('/admin/main_hotel/', methods=['GET'])
@app.route('/admin/main_hotel/<string:message>', methods=['GET'])
def hotel_search_html(message=None):
    email = session.get('email')  # 取session
    if email:
        login = True
        if message:
            return render_template('skike_hotel_search.html',KR_location_list = KR_location_list,today = today, next_week = next_week, login =login,message=message)
        return render_template('skike_hotel_search.html',KR_location_list = KR_location_list,today = today, next_week = next_week, login =login)
        # return 'welcome %s' % username
    else:
        return redirect(url_for("user_sign_in"))
    # return render_template('skike_hotel_search.html',KR_location_list = KR_location_list,today = today, tomorrow = tomorrow)

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
        acceess_expire = ACCESS_EXPIRE
        sign_up_data = check_exist_user(rdsDB,email)
        picture =""
        if sign_up_data:
            error = "A person with this email or name already exists, please try another email name"
            return render_template('user_register.html',message = error)
        else:
            if provider =="native":
                insert_register_data(rdsDB,provider, name, email,hashed_password, picture,acceess_expire)
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
        sign_data = insert_signin_data(rdsDB,email)
        if sign_data:
            if check_password(password_form, sign_data["password"]):
                session['email'] = email
                session['uid'] = random.randint(0, 100)
                return redirect(url_for('main_index'))
            else:
                error = "Can't recognite this user/id please try again"
                return render_template('user_login.html',message = error)
        elif sign_data ==None:
            error = "Can't recognite this user/id please try again"
            return render_template('user_login.html',message = error)
        error = "Can't search this user/id please try again"
    return render_template('user_login.html',message = error)

@app.route('/api/1.0/hotel/search/', methods=['POST','GET'])
def hotel_search():
    email = session.get('email')  
    if email:
        login = True
        form_data = request.form
        location = form_data['location']
        start_date = form_data['start_date']
        end_date = form_data['end_date']
        if start_date>end_date:
            message ="想搜尋日期不能大於日期結尾,請在搜尋一次"
            return redirect(url_for("hotel_search_html",message=message))
        sql_result = get_hotel_search_list(rdsDB,start_date,end_date,location)
        sql_count_result = get_hotel_search_coount(rdsDB,start_date,end_date,location)
        sum = 0
        for item in sql_count_result:
            sum+=item['count(distinct(name))']
        return render_template('skike_hotel.html', hotel_list=sql_result, start_date= start_date, end_date = end_date, location = location,sum = sum,login =login)
    else:
        return redirect(url_for("user_sign_in"))
@app.route('/api/1.0/hotel/search/<location>', methods=['GET'])
def hotel_search_title_get(location):
    email = session.get('email')
    if email:
        login = True
        start_date = date.today()
        end_date = date.today()+timedelta(7)
        method = "hotel_search_title_get"
        sql_result = get_hotel_search(rdsDB,start_date,end_date,location)
        sql_count_result = get_hotel_search_number(rdsDB,start_date,end_date,location)
        sum = 0
        for item in sql_count_result:
            sum+=item['count(distinct(name))']
        return render_template('skike_hotel.html', hotel_list=sql_result, start_date= start_date, end_date = end_date, location = location, method = method, sum =sum, login =login)
    else:
        return redirect(url_for("user_sign_in"))
@app.route('/route_function',methods=[ "GET",'POST'])
def route_function():
    if request.form.get('delete_user_page'):
        email = session.get('email')
        hotel_name = request.form.get('hotel_name')
        delete_user_favorite_item(conn, email, hotel_name= hotel_name)
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
    # print(request.form.get('status'))
    if request.form.get('status'):
        delete_user_favorite_item(conn, email, hotel_detail = hotel_detail, hotel_img=hotel_img)
    else:
        add_user_favorite_item(conn, email, want_time_start, want_time_end\
            , hotel_name,hotel_img,hotel_detail,user_name,location,price)
    return "ok"
@app.route('/api/1.0/hotel/search/<start_date>/<end_date>/<location>/<condition>', methods=['GET'])
###sort by price, comment count, comment score###
def hotel_search_get(start_date,end_date,location,condition):
    condition1 = condition.split(',')
    condition1 = condition1[0]
    condition2 = condition.split(',')
    condition2 = condition2[1]
    sql_result = get_re_sort_result(rdsDB, start_date,end_date,location,condition1,condition2)
    return render_template('skike_hotel.html', hotel_list=sql_result, start_date= start_date, end_date = end_date, location = location)
@app.route('/api/1.0/air_plane/search_get', methods=['POST','GET'])   
def airplane_search_func():
    email = session.get('email')
    if email:
        login = True
        form_data = request.form
        # round = form_data['round'] #no use now
        location = form_data['location']
        location_arrive = form_data['location_arrive']
        start_date = form_data['start_date']
        select_adult = form_data['adults_number']

        sql_result = get_flight_ticket_plan(rdsDB,start_date,location_arrive,location)
        # add_flight_pic_url(sql_result)
        sql_get =[]
        get_moregrade_price(rdsDB,sql_get,sql_result,start_date,select_adult)
        return render_template('skike_flight.html', flight_list=sql_get, today =today, tomorrow= tomorrow,start_date = start_date, location =location,location_arrive =location_arrive,login =login)
    else:
        return redirect(url_for("user_sign_in"))

@app.route('/api/1.0/hotel/<int:id>/<float:geocode_lat>/<float:geocode_lng>/<string:start_date>', methods=['GET','POST'])
def hotel_detail(id, geocode_lat,geocode_lng,start_date):
    cursor = rdsDB.cursor()
    email = session.get('email')  
    if email:
        login = True
        if request.method == 'POST':
            airport_alter = request.form['airport_alter']
            result_sql_geocode = get_nearest_airport(rdsDB,airport_alter)['result_sql_geocode']
        elif request != "POST":
            print("here")
            geo_result = get_airport_list(rdsDB,geocode_lat,geocode_lng,MAX_NUMBER)["geo_result"]
            near_airport_lat = get_airport_list(rdsDB,geocode_lat,geocode_lng,MAX_NUMBER)["near_airport_lat"]
            near_airport_lng = get_airport_list(rdsDB,geocode_lat,geocode_lng,MAX_NUMBER)["near_airport_lng"]
            print(geo_result,near_airport_lat,near_airport_lng)
        sql_agency = "SELECT distinct (hotel_agency) FROM skike.hotel inner join skike.hotel_alternative on hotel.id =hotel_alternative.hotel_id where hotel.id = '{}' order by hotel_alternative.hotel_agency;".format(str(id))
        cursor.execute(sql_agency)
        result_agency = cursor.fetchall()
        sql_sub = "SELECT * FROM skike.hotel where id = '{}'".format(str(id))
        cursor.execute(sql_sub)
        result_sub = cursor.fetchall()
        sql_name = result_sub[0:1]
        result_sub_2 = get_hotel_alter(start_date, id)
        agency_list = result_sub_2['agency']
        num_result_sub_2 = len(result_sub_2['newlist'])
        result_sub_2 = result_sub_2['newlist']
        sql_name = result_sub[0:1]
        url = "https://maps.googleapis.com/maps/api/directions/json?language=zh-TW&origin={},{}&destination={},{}&mode=transit&key={}".format(near_airport_lat,near_airport_lng,geocode_lat,geocode_lng,config.GOOGLE_API_KEY)
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        result = response.json()
        if result['status'] =='ZERO_RESULTS':
            error_msg = "The direction service is not support for this airport the hotel"
            flash("")
            return redirect(url_for('hotel_detail',id=id, geocode_lat=geocode_lat,geocode_lng=geocode_lng,start_date=start_date,error_msg=error_msg))
        elif result['status'] =='REQUEST_DENIED':
            print('enter api denied')
            return render_template('skike_hotel_detail_origin.html',detail_hotel_list = result_sub_2, sql_name = sql_name, google_api = config.GOOGLE_API_KEY, agency_list = agency_list ,start_date = start_date,id=id,num_result_sub_2 = num_result_sub_2)
        direction_list =[]
        geo_list = []
        route_flow = []
        print("-----------------------------------------")
        translator = Translator()
        arrival_time = result['routes'][0]['legs'][0]["arrival_time"]["value"]
        departure_time = result['routes'][0]['legs'][0]["departure_time"]["value"]
        go_list=[]
        date_time = datetime.fromtimestamp(arrival_time)
        date_time_depart = datetime.fromtimestamp(departure_time)
        need_time = int(arrival_time-departure_time)
        need_hour = int(need_time/HOUR_IN_SECOND)
        need_min = int((need_time-HOUR_IN_SECOND*need_hour)/MINUTE_IN_SECOND)
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
            j = result['routes'][0]['legs'][0]['steps'][i]['html_instructions'] 
            route_flow.append(j)
            geo_list.append(polyline.decode(result['routes'][0]['legs'][0]['steps'][i]["polyline"]['points']))
        go_list.append(d_arrival_time)
        route_flow2 = dict(zip(route_flow, go_list))
        print(123)
        return render_template('skike_hotel_detail_origin.html',detail_hotel_list = result_sub_2, result_agency = result_agency, sql_name = sql_name, google_api = config.GOOGLE_API_KEY,direction_list = direction_list, test_code = geo_list, geocode=result_sql_geocode,geocode_lat = geocode_lat,geocode_lng=geocode_lng,route_flow2 = route_flow2, geo_result = geo_result, today = today, tomorrow = tomorrow,agency_list =agency_list, start_date = start_date,id=id,num_result_sub_2 = num_result_sub_2,start_time = date_time_depart,login =login,need_hour=need_hour,need_min =need_min)
    else:
        return redirect(url_for("user_sign_in"))
@app.route('/route_function/hotel_detail',methods=[ "GET",'POST'])
def route_function_hotel_detail():
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
    return result_sub_2