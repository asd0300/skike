from flask.globals import session
from flask_login import LoginManager, UserMixin, login_user,\
    logout_user, login_required, current_user
import bcrypt
from datetime import datetime, timedelta, date
from pymongo import MongoClient
from flask import render_template, request, redirect, url_for, flash
from server import app
from server.models.user_model import check_exist_user, insert_register_data,\
    insert_signin_data, connect_skike_db, get_user_page_data
from server.env import config
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

conn = MongoClient(
    "mongodb://{}:{}@ec2-18-223-232-121.us-east-2.compute.amazonaws.com:27017/?\
    authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl\
    =false".format(
                  config.MONGO_PASS_SKIKE_SKIKE_ORIGIN_ACCOUNT,
                  config.MONGO_PASS_SKIKE_SKIKE_ORIGIN_PASS))
rds_db = connect_skike_db()
cursor = rds_db.cursor()
sql_sub = "SELECT email FROM skike.user ;"
cursor.execute(sql_sub)
emails = cursor.fetchall()
emails = [item['email'] for item in emails]

login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = 'check in'


def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password.encode('utf8'), bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf8'),
                          hashed_password.encode('utf8'))


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
    user_id = request.form.get('email')
    if user_id not in emails:
        return
    user = User()
    user.id = user_id

    user.is_authenticated = \
        (request.form['password'] == emails[user_id]['password'])

    return user


@app.route('/sign_out')
def sign_out():
    # email = current_user.get_id()
    # logout_user()
    email = session['email']
    session.clear()
    return redirect(url_for('user_sign_in'))


@app.route('/admin/user_page/', methods=['GET'])
def user_page():
    """user"""
    email = session.get('email')
    if email:
        email = session['email']
        results = get_user_page_data(conn, email)
        print(session['email'])
        return render_template(
            'user_page.html',
            korea_location_list=config.korea_location_list,
            today=TODAY,
            tomorrow=TOMORROW,
            sql_favorite_result_hotel=results,
            email=email)


@app.route('/admin/user', methods=['GET'])
def user_sign_up():
    """director"""
    return render_template('user_register.html')

@app.route('/')
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
        sign_up_data = check_exist_user(email)
        picture = ""
        if sign_up_data:
            error = "A person with this email or name \
                already exists, please try another email name"
            flash(error)
            return redirect(url_for('user_sign_in'))
        if provider == "native":
            insert_register_data(
                provider,
                name,
                email,
                hashed_password,
                picture,
                acceess_expire)
        message = "Account create ok, please sign in again"
        return render_template(
            'user_login.html',
            message=message)


@app.route('/user/sign_in', methods=['POST', 'GET'])
def login():
    """login"""
    if request.method == 'GET':
        return redirect(url_for('main_index'))
    if request.method == 'POST':
        user_details = request.form
        email = user_details['email']
        password_form = user_details['password']
        sign_data = insert_signin_data(email)
        if sign_data:
            if check_password(password_form, sign_data["password"]):
                session['email'] = email
                return redirect(url_for('main_index'))
        error = "Please check your email/password again"
        session['m'] = "fail"
        # return render_template('user_login.html',message=error)
        flash(error)
        return redirect(url_for('user_sign_in'))