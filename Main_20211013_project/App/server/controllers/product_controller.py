"""skike"""
from datetime import datetime, timedelta, date
from flask import render_template, request, redirect, url_for
from server import app
from server.models.product_model import get_hotel_alter, \
    get_hotel_search_list,\
    get_hotel_search_coount, get_hotel_search, get_hotel_search_number, \
    get_re_sort_result,\
    get_flight_ticket_plan, get_moregrade_price, get_nearest_airport,\
    get_airport_list, get_hotel_detail_title_info, delete_user_favorite_item,\
    get_google_direction, add_user_favorite_item, get_hotel_more_pic
from server.env import config
from flask_login import login_required, current_user
# from ..env import config
SECRET_KEY = config.SECRET_KEY
app.secret_key = config.SECRET_KEY
ACCESS_EXPIRE = config.ACCESS_EXPIRE
MAX_NUMBER = config.MAX_NUMBER
HOUR_IN_SECOND = config.HOUR_IN_SECOND
MINUTE_IN_SECOND = config.MINUTE_IN_SECOND


TODAY = str(date.today())
TOMORROW = str(date.today()+timedelta(days=1))
NEXT_WEEK = str(date.today()+timedelta(days=7))


@app.route('/')
@app.route('/admin/main_flight/', methods=['GET'])
@login_required
def main_index():
    """main"""
    return render_template(
                          'main.html',
                          korea_location_list=config.korea_location_list,
                          today=TODAY,
                          tomorrow=TOMORROW)


@app.route('/admin/main_hotel/', methods=['GET'])
@app.route('/admin/main_hotel/<string:message>', methods=['GET'])
@login_required
def hotel_search_html(message=None):
    """main hotel"""
    if message:
        return render_template(
                          'skike_hotel_search.html',
                          korea_location_list=config.korea_location_list,
                          today=TODAY,
                          tomorrow=TOMORROW,
                          next_week=NEXT_WEEK,
                          message=message)
    return render_template(
                          'skike_hotel_search.html',
                          korea_location_list=config.korea_location_list,
                          today=TODAY,
                          tomorrow=TOMORROW,
                          next_week=NEXT_WEEK)


@app.route('/api/1.0/hotel/search/', methods=['POST', 'GET'])
@login_required
def hotel_search():
    """search bar hotel"""
    form_data = request.form
    location = form_data['location']
    start_date = form_data['start_date']
    end_date = form_data['end_date']
    if start_date > end_date:
        message = "想搜尋日期不能大於日期結尾,請在搜尋一次"
        return redirect(url_for("hotel_search_html", message=message))
    sql_result = get_hotel_search_list(start_date, end_date, location)
    sql_count_result_single_hotel = get_hotel_search_coount(start_date, end_date, location)
    searched_hotel_count = 0
    for item in sql_count_result_single_hotel:
        searched_hotel_count += item['count(distinct(name))']
    return render_template(
        'skike_hotel.html',
        hotel_list=sql_result,
        start_date=start_date,
        tomorrow = TOMORROW,
        end_date=end_date,
        location=location,
        searched_hotel_count=searched_hotel_count)


@app.route('/api/1.0/hotel/search/<location>', methods=['GET'])
@login_required
def hotel_search_title_get(location):
    """title search"""
    start_date = TOMORROW
    end_date = date.today()+timedelta(7)
    method = "hotel_search_title_get"
    sql_result = get_hotel_search(start_date, end_date, location)
    sql_count_result_single_hotel = get_hotel_search_number(start_date, end_date, location)
    searched_hotel_count = 0
    for item in sql_count_result_single_hotel:
        searched_hotel_count += item['count(distinct(name))']
    return render_template(
        'skike_hotel.html',
        hotel_list=sql_result,
        start_date=start_date,
        end_date=end_date,
        location=location,
        method=method,
        searched_hotel_count=searched_hotel_count,
        next_week=NEXT_WEEK,
        today=TODAY)


@app.route('/api/1.0/hotel/search/<start_date>/<end_date>/\
    <location>/<condition>', methods=['GET'])
@login_required
def hotel_search_get(start_date, end_date, location, condition):
    """sorter"""
    search_condition = condition.split(',')
    condition_search = search_condition[0]
    condition_sort = search_condition[1]
    sql_result = get_re_sort_result(start_date, end_date,
                                    location, condition_search, condition_sort)
    return render_template(
        'skike_hotel.html',
        hotel_list=sql_result,
        start_date=start_date,
        end_date=end_date,
        location=location)


@app.route('/api/1.0/air_plane/search_get', methods=['POST', 'GET'])
@login_required
def airplane_search_func():
    """airplane_search_func"""
    form_data = request.form
    # round = form_data['round'] #no use now
    location = form_data['location']
    location_arrive = form_data['location_arrive']
    start_date = form_data['start_date']
    select_adult = form_data['adults_number']
    
    sql_result = get_flight_ticket_plan(start_date, location_arrive, location)
    # add_flight_pic_url(sql_result)
    # sql_get = []
    flight_list = get_moregrade_price(sql_result, start_date, select_adult)
    return render_template('skike_flight.html',
                          flight_list=flight_list,
                          today=TODAY,
                          tomorrow=TOMORROW,
                          start_date=start_date,
                          location=location,
                          location_arrive=location_arrive)


@app.route('/api/1.0/hotel/<int:id>/<float:geocode_lat>/<float:geocode_lng>/\
    <string:start_date>', methods=['GET', 'POST'])
@login_required
def hotel_detail(id, geocode_lat, geocode_lng, start_date):
    """hotel_detail"""
    login = True
    if request.method == 'POST':
        airport_alter = request.form['airport_alter']
        nearest_result = get_nearest_airport(airport_alter)
        near_airport_lat = nearest_result['near_airport_lat']
        near_airport_lng = nearest_result['near_airport_lng']
        geo_result = nearest_result['geo_result']
    elif request.method != "POST":
        airport_result = get_airport_list(geocode_lat, geocode_lng, MAX_NUMBER)
        geo_result = airport_result['geo_result']
        near_airport_lat = airport_result['near_airport_lat']
        near_airport_lng = airport_result['near_airport_lng']
    sql_name = get_hotel_detail_title_info(id)
    full_hotel_alter_information = get_hotel_alter(start_date, id)
    agency_list = full_hotel_alter_information['agency']
    result_count_of_agency = len(full_hotel_alter_information['newlist'])
    full_hotel_alter_information = full_hotel_alter_information['newlist']
    google_result = get_google_direction(near_airport_lat, near_airport_lng,
                                         geocode_lat, geocode_lng,
                                         config.GOOGLE_API_KEY,
                                         HOUR_IN_SECOND, MINUTE_IN_SECOND)
    geo_list = google_result['geo_list']
    need_hour = google_result["need_hour"]
    need_min = google_result["need_min"]

    date_time_depart = google_result["date_time_depart"]
    google_direction_transit_information = google_result["route_flow2"]
    return render_template(
                        'skike_hotel_detail_origin.html',
                        detail_hotel_list=full_hotel_alter_information,
                        sql_name=sql_name,
                        google_api=config.GOOGLE_API_KEY,
                        test_code=geo_list,
                        geocode_lat=geocode_lat,
                        geocode_lng=geocode_lng,
                        google_direction_transit_information=google_direction_transit_information,
                        geo_result=geo_result,
                        today=TODAY,
                        tomorrow=TOMORROW,
                        agency_list=agency_list,
                        start_date=start_date,
                        id=id,
                        result_count_of_agency=result_count_of_agency,
                        start_time=date_time_depart,
                        login=login,
                        need_hour=need_hour,
                        need_min=need_min)


@app.route('/route_function/hotel_detail', methods=["GET", 'POST'])
def route_function_hotel_detail():
    """recheck agency"""
    fetch_checkbox_information = request.form.get('checkbox')
    agency_selected = request.form.get('agency_selected')
    start_date = request.form.get('start_date')
    id = request.form.get('id')
    agency_result = request.form.get('agency_result')
    result_feature = fetch_checkbox_information.split('|')
    while '' in result_feature:
        result_feature.remove('')
    feature_dict = {'checkbox': result_feature, 'agency_selected': agency_selected}
    full_hotel_alter_information = get_hotel_alter(start_date,
                                   id,
                                   feature_dict=feature_dict,
                                   agency_result=agency_result)
    result_count_of_agency = len(full_hotel_alter_information['newlist'])
    full_hotel_alter_information['result_count_of_agency'] = result_count_of_agency
    return full_hotel_alter_information


@app.route('/route_function', methods=["GET", 'POST'])
@login_required
def route_function():
    """favorite item function"""
    if request.form.get('delete_user_page'):
        email = current_user.get_id()
        hotel_name = request.form.get('hotel_name')
        delete_user_favorite_item(email, hotel_name=hotel_name)
        return"ok"
    hotel_name = request.form.get('the_name')
    want_time_start = request.form.get('want_time_start')
    want_time_end = request.form.get('want_time_end')
    hotel_feature = request.form.get('hotel_detail')
    hotel_img = request.form.get('hotel_img')
    email = email = current_user.get_id()
    location = request.form.get('location')
    price = request.form.get('price')
    price = int(''.join([x for x in price if x.isdigit()]))
    user_name = "test"
    if request.form.get('status'):
        delete_user_favorite_item(email, hotel_detail=hotel_feature,
                                  hotel_img=hotel_img)
    else:
        add_user_favorite_item(email, want_time_start, want_time_end,
                               hotel_name, hotel_img, hotel_feature,
                               user_name, location, price)
    return "ok"

@app.route('/hotel/search/more_picture',methods=[ "GET",'POST'])
def hotel_more_picture():
    print(request.form)
    hotel_id = request.form.get('hotel_id')
    want_time_start = request.form.get('want_time_start')
    want_time_end = request.form.get('want_time_end')
    print(hotel_id,want_time_start,want_time_end)
    pic_list = get_hotel_more_pic(hotel_id,want_time_start,want_time_end)
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