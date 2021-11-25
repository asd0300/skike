"""skike"""
from datetime import datetime, timedelta,date
import random
import pymysql
from flask import render_template,request,redirect,session,url_for
from pymongo import MongoClient
from server import app
from server.models.product_model import get_hotel_alter,check_exist_user,insert_register_data\
    ,insert_signin_data,get_hotel_search_list,get_hotel_search_coount,\
    get_user_page_data,get_hotel_search,get_hotel_search_number,\
    delete_user_favorite_item,add_user_favorite_item,get_re_sort_result,\
    get_flight_ticket_plan,get_moregrade_price,get_nearest_airport,\
    get_airport_list,get_hotel_detail_title_info\
    ,get_google_direction
from server.env import config
import bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user



SECRET_KEY = config.SECRET_KEY
from ..env import config
###flask-login###
app.secret_key = config.SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = '請證明你並非來自黑暗草泥馬界'


rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
            user="admin",password=config.RDSMASTERPASSWORD,\
            port=config.RDSPORT,database="skike",\
            cursorclass = pymysql.cursors.DictCursor)

cursor = rdsDB.cursor()
sql_sub = "SELECT email FROM skike.user ;"
cursor.execute(sql_sub)
emails = cursor.fetchall()
emails = [item['email'] for item in emails]
###################
class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in emails:
        return

    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    user_id = request.form.get('user_id')
    if user_id not in emails:
        return
    
    user = User()
    user.id = user_id

    user.is_authenticated = (request.form['password'] == emails[user_id]['password'])

    return user
#################



ACCESS_EXPIRE = config.ACCESS_EXPIRE
MAX_NUMBER = config.MAX_NUMBER
HOUR_IN_SECOND = config.HOUR_IN_SECOND
MINUTE_IN_SECOND = config.MINUTE_IN_SECOND


conn = MongoClient("mongodb://{}:{}@ec2-18-223-232-121.us-east-2.compute.amazonaws.com:27017/?\
    authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl\
    =false".format(config.MONGO_PASS_SKIKE_SKIKE_ORIGIN_ACCOUNT,\
    config.MONGO_PASS_SKIKE_SKIKE_ORIGIN_PASS))

KR_location_list = [k for k,v in config.locLN_KR.items()]
TODAY = str(date.today())
TOMORROW = str(date.today()+timedelta(days=1))
NEXT_WEEK = str(date.today()+timedelta(days=7))
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
# @login_required
def main_index():
    """main"""
    # if current_user.is_active:
    # email = session.get('email')  # 取session
    return render_template('main.html',KR_location_list =\
            KR_location_list,today = TODAY, tomorrow = TOMORROW)
    #     # return 'welcome %s' % username
    return render_template('main.html',KR_location_list =\
                KR_location_list,today = TODAY, tomorrow = TOMORROW)

@app.route('/sign_out')
def sign_out():
    user_id = current_user.get_id()
    logout_user()
    return redirect(url_for('user_sign_in'))

@app.route('/admin/user_page/', methods=['GET'])
def user_page():
    """user"""
    email = session.get('email')  # 取session
    if email:
        login = True
        results = get_user_page_data(conn,email)
        print(results)
        return render_template('user_page.html',KR_location_list =\
            KR_location_list,today = TODAY, tomorrow = TOMORROW, login =login\
            ,sql_favorite_result_hotel=results,email=email)
    return redirect(url_for("user_sign_in"))

@app.route('/admin/main_hotel/', methods=['GET'])
@app.route('/admin/main_hotel/<string:message>', methods=['GET'])
def hotel_search_html(message=None):
    """main hotel"""
    email = session.get('email')  # 取session
    if email:
        login = True
        if message:
            return render_template('skike_hotel_search.html',KR_location_list =\
            KR_location_list,today = TODAY, next_week = NEXT_WEEK, login =login\
            ,message=message)
        return render_template('skike_hotel_search.html',KR_location_list =\
            KR_location_list,today = TODAY, next_week = NEXT_WEEK, login =login)
        # return 'welcome %s' % username
    return redirect(url_for("user_sign_in"))

@app.route('/admin/user', methods=['GET'])
def user_sign_up():
    """director"""
    return render_template('user_register.html')
@app.route('/admin/user_login', methods=['GET'])
def user_sign_in():
    """director"""
    return render_template('user_login.html')
@app.route('/user/sign_up', methods=['GET', 'POST'])
def register():
    """register"""
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
        if provider =="native":
            insert_register_data(rdsDB,provider, name,\
            email,hashed_password, picture,acceess_expire)
        message ="Account create ok, please sign in again"
        return render_template('user_login.html',message=message)

@app.route('/user/sign_in', methods=['POST','GET'])
def login():
    # """login"""
    # if request.method == 'POST' :
    #     user_details = request.form
    #     email = user_details['email']
    #     password_form = user_details['password']
    #     sign_data = insert_signin_data(rdsDB,email)
    #     if sign_data:
    #         if check_password(password_form, sign_data["password"]):
    #             session['email'] = email
    #             session['uid'] = random.randint(0, 100)
    #             return redirect(url_for('main_index'))
    #         error = "Can't recognite this user/id please try again"
    #         return render_template('user_login.html',message = error)
    #     elif sign_data is None:
    #         error = "Can't recognite this user/id please try again"
    #         return render_template('user_login.html',message = error)
    #     error = "Can't search this user/id please try again"
    # return render_template('user_login.html',message = error)
    if request.method == 'GET':  
        return render_template('user_login.html') 
    if request.method == 'POST' :
        user_details = request.form
        email = user_details['email']
        password_form = user_details['password']
        sign_data = insert_signin_data(rdsDB,email)
        if sign_data:
            if check_password(password_form, sign_data["password"]):
                user = User()
                user.id = email
                login_user(user)
                return redirect(url_for('main_index'))
            error = "Can't recognite this user/id please try again"
            return render_template('user_login.html',message = error)
@app.route('/api/1.0/hotel/search/', methods=['POST','GET'])
def hotel_search():
    """search bar hotel"""
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
        sum2 = 0
        for item in sql_count_result:
            sum2+=item['count(distinct(name))']
        return render_template('skike_hotel.html', hotel_list=sql_result,\
            start_date= start_date, end_date = end_date, location =\
            location,sum2 = sum2,login =login)
    return redirect(url_for("user_sign_in"))
@app.route('/api/1.0/hotel/search/<location>', methods=['GET'])
def hotel_search_title_get(location):
    """title search"""
    email = session.get('email')
    if email:
        login = True
        start_date = date.today()
        end_date = date.today()+timedelta(7)
        method = "hotel_search_title_get"
        sql_result = get_hotel_search(rdsDB,start_date,end_date,location)
        sql_count_result = get_hotel_search_number(rdsDB,start_date,end_date,location)
        sum2 = 0
        for item in sql_count_result:
            sum2+=item['count(distinct(name))']
        return render_template('skike_hotel.html', hotel_list=sql_result, start_date=\
            start_date, end_date = end_date, location = location, method = method, sum2=sum2\
            , login =login,next_week=NEXT_WEEK,today = TODAY)
    return redirect(url_for("user_sign_in"))
@app.route('/route_function',methods=[ "GET",'POST'])
def route_function():
    """favorite item function"""
    if request.form.get('delete_user_page'):
        email = session.get('email')
        hotel_name = request.form.get('hotel_name')
        delete_user_favorite_item(conn, email, hotel_name= hotel_name)
        return"ok"
    hotel_name = request.form.get('the_name')
    want_time_start = request.form.get('want_time_start')
    want_time_end = request.form.get('want_time_end')
    hotel_detail2 = request.form.get('hotel_detail')
    hotel_img = request.form.get('hotel_img')
    email = session.get('email')
    location = request.form.get('location')
    price = request.form.get('price')
    price =int(''.join([x for x in price if x.isdigit()]))
    user_name= "test"
    # print(request.form.get('status'))
    if request.form.get('status'):
        delete_user_favorite_item(conn, email, hotel_detail = hotel_detail2, hotel_img=hotel_img)
    else:
        add_user_favorite_item(conn, email, want_time_start, want_time_end\
            , hotel_name,hotel_img,hotel_detail2,user_name,location,price)
    return "ok"
@app.route('/api/1.0/hotel/search/<start_date>/<end_date>/<location>/<condition>', methods=['GET'])
###sort by price, comment count, comment score###
def hotel_search_get(start_date,end_date,location,condition):
    """get hotel name"""
    login =True
    condition1 = condition.split(',')
    condition1 = condition1[0]
    condition2 = condition.split(',')
    condition2 = condition2[1]
    sql_result = get_re_sort_result(rdsDB, start_date,end_date,location,condition1,condition2)
    return render_template('skike_hotel.html', hotel_list=sql_result,\
        start_date= start_date, end_date = end_date, location = location,login=login)
@app.route('/api/1.0/air_plane/search_get', methods=['POST','GET'])
def airplane_search_func():
    """airplane_search_func"""
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
        return render_template('skike_flight.html', flight_list=sql_get, today =TODAY, tomorrow= TOMORROW,start_date = start_date, location =location,location_arrive =location_arrive,login =login)
    return redirect(url_for("user_sign_in"))

@app.route('/api/1.0/hotel/<int:id>/<float:geocode_lat>/<float:geocode_lng>/<string:start_date>', methods=['GET','POST'])
def hotel_detail(id, geocode_lat,geocode_lng,start_date):
    """hotel_detail"""
    email = session.get('email')  
    if email:
        login = True
        if request.method == 'POST':
            airport_alter = request.form['airport_alter']
            nearest_result =get_nearest_airport(rdsDB,airport_alter)
            near_airport_lat = nearest_result['near_airport_lat']
            near_airport_lng = nearest_result['near_airport_lng']
            geo_result = nearest_result['geo_result']
        elif request != "POST":
            airport_result =get_airport_list(rdsDB,geocode_lat,geocode_lng,MAX_NUMBER)
            geo_result =airport_result['geo_result']
            near_airport_lat =airport_result['near_airport_lat']
            near_airport_lng =airport_result['near_airport_lng']
        sql_name = get_hotel_detail_title_info(rdsDB,id)
        result_sub_2 = get_hotel_alter(start_date, id)
        agency_list = result_sub_2['agency']
        result_count_of_agency = len(result_sub_2['newlist'])
        result_sub_2 = result_sub_2['newlist']
        google_result = get_google_direction(near_airport_lat,near_airport_lng,geocode_lat,geocode_lng,config.GOOGLE_API_KEY,HOUR_IN_SECOND,MINUTE_IN_SECOND)
        geo_list = google_result['geo_list']
        need_hour = google_result["need_hour"]
        need_min = google_result["need_min"]
        date_time_depart = google_result["date_time_depart"]
        route_flow2 = google_result["route_flow2"]
        return render_template('skike_hotel_detail_origin.html',detail_hotel_list = result_sub_2, sql_name = sql_name, google_api = config.GOOGLE_API_KEY, test_code = geo_list,geocode_lat = geocode_lat,geocode_lng=geocode_lng,route_flow2 = route_flow2, geo_result = geo_result, today = TODAY, tomorrow = TOMORROW,agency_list =agency_list, start_date = start_date,id=id,result_count_of_agency = result_count_of_agency,start_time = date_time_depart,login =login,need_hour=need_hour,need_min =need_min)
    return redirect(url_for("user_sign_in"))
@app.route('/route_function/hotel_detail',methods=[ "GET",'POST'])
def route_function_hotel_detail():
    """recheck agency"""
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
    result_count_of_agency = len(result_sub_2['newlist'])
    result_sub_2['result_count_of_agency']= result_count_of_agency
    return result_sub_2