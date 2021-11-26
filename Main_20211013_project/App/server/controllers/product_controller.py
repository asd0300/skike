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
    get_google_direction, add_user_favorite_item
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
                          next_week=NEXT_WEEK,
                          message=message)
    return render_template(
                          'skike_hotel_search.html',
                          korea_location_list=config.korea_location_list,
                          today=TODAY,
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
    sql_count_result = get_hotel_search_coount(start_date, end_date, location)
    sum2 = 0
    for item in sql_count_result:
        sum2 += item['count(distinct(name))']
    return render_template(
        'skike_hotel.html',
        hotel_list=sql_result,
        start_date=start_date,
        end_date=end_date,
        location=location,
        sum2=sum2)


@app.route('/api/1.0/hotel/search/<location>', methods=['GET'])
@login_required
def hotel_search_title_get(location):
    """title search"""
    start_date = date.today()
    end_date = date.today()+timedelta(7)
    method = "hotel_search_title_get"
    sql_result = get_hotel_search(start_date, end_date, location)
    sql_count_result = get_hotel_search_number(start_date, end_date, location)
    sum2 = 0
    for item in sql_count_result:
        sum2 += item['count(distinct(name))']
    return render_template(
        'skike_hotel.html',
        hotel_list=sql_result,
        start_date=start_date,
        end_date=end_date,
        location=location,
        method=method,
        sum2=sum2,
        next_week=NEXT_WEEK,
        today=TODAY)


@app.route('/api/1.0/hotel/search/<start_date>/<end_date>/\
    <location>/<condition>', methods=['GET'])
@login_required
def hotel_search_get(start_date, end_date, location, condition):
    """get hotel name"""
    condition1 = condition.split(',')
    condition1 = condition1[0]
    condition2 = condition.split(',')
    condition2 = condition2[1]
    sql_result = get_re_sort_result(start_date, end_date,
                                    location, condition1, condition2)
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
    sql_get = []
    get_moregrade_price(sql_get, sql_result, start_date, select_adult)
    return render_template(
                          'skike_flight.html',
                          flight_list=sql_get,
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
    elif request != "POST":
        airport_result = get_airport_list(geocode_lat, geocode_lng, MAX_NUMBER)
        geo_result = airport_result['geo_result']
        near_airport_lat = airport_result['near_airport_lat']
        near_airport_lng = airport_result['near_airport_lng']
    sql_name = get_hotel_detail_title_info(id)
    print(start_date, id)
    result_sub_2 = get_hotel_alter(start_date, id)
    agency_list = result_sub_2['agency']
    result_count_of_agency = len(result_sub_2['newlist'])
    result_sub_2 = result_sub_2['newlist']
    google_result = get_google_direction(near_airport_lat, near_airport_lng,
                                         geocode_lat, geocode_lng,
                                         config.GOOGLE_API_KEY,
                                         HOUR_IN_SECOND, MINUTE_IN_SECOND)
    geo_list = google_result['geo_list']
    need_hour = google_result["need_hour"]
    need_min = google_result["need_min"]

    date_time_depart = google_result["date_time_depart"]
    route_flow2 = google_result["route_flow2"]
    return render_template(
                        'skike_hotel_detail_origin.html',
                        detail_hotel_list=result_sub_2,
                        sql_name=sql_name,
                        google_api=config.GOOGLE_API_KEY,
                        test_code=geo_list,
                        geocode_lat=geocode_lat,
                        geocode_lng=geocode_lng,
                        route_flow2=route_flow2,
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
    checkbox = request.form.get('checkbox')
    agency_selected = request.form.get('agency_selected')
    start_date = request.form.get('start_date')
    id = request.form.get('id')
    agency_result_1st = request.form.get('agency_result')
    result_feature = checkbox.split('|')
    while '' in result_feature:
        result_feature.remove('')
    feature_dict = {}
    feature_dict['checkbox'] = result_feature
    feature_dict['agency_selected'] = agency_selected

# feature_dict = {
#     "checkbos": result_feature
# }

    result_sub_2 = get_hotel_alter(start_date,
                                   id,
                                   feature_dict=feature_dict,
                                   agency_result_1st=agency_result_1st)
    result_count_of_agency = len(result_sub_2['newlist'])
    result_sub_2['result_count_of_agency'] = result_count_of_agency
    return result_sub_2


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
    hotel_detail2 = request.form.get('hotel_detail')
    hotel_img = request.form.get('hotel_img')
    email = email = current_user.get_id()
    location = request.form.get('location')
    price = request.form.get('price')
    price = int(''.join([x for x in price if x.isdigit()]))
    user_name = "test"
    if request.form.get('status'):
        delete_user_favorite_item(email, hotel_detail=hotel_detail2,
                                  hotel_img=hotel_img)
    else:
        add_user_favorite_item(email, want_time_start, want_time_end,
                               hotel_name, hotel_img, hotel_detail2,
                               user_name, location, price)
    return "ok"
