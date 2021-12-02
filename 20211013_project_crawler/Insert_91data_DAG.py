from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import random
from pymongo import MongoClient
import concurrent.futures
from env import config
from datetime import  datetime,timedelta,date
import pymysql
import string
import numpy

default_args = {
    'owner': 'airflow2',
    'depends_on_past': False,
    'start_date' : datetime(year=2021, month=12, day=2, hour=16, minute=30),
    'email' : ['fan0300@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries' : 1,
    'retry_delay': timedelta(minutes =1)
}
dag = DAG(
    '91app_mock_data',
    default_args = default_args,
    description= 'mock_data_of_91app',
    schedule_interval = '30 16 * * *'
)

def insert_return_id():
    rds_DB = pymysql.connect(host=config.RDSHOSTNAME,\
                            user="admin",password=config.RDSMASTERPASSWORD,\
                            port=3306,database="stylish",\
                            cursorclass = pymysql.cursors.DictCursor)
    cursor = rds_DB.cursor()
    return_number = random.randint(700,800)
    date_yesterday = datetime.now()+timedelta(days=-1)
    datenow_str_yesterday = date_yesterday.strftime("%Y-%m-%d")
    sql = "SELECT distinct(cid) FROM stylish.data91app  where date = '{}' limit {};".format(datenow_str_yesterday, return_number)
    rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
                            user="admin",password=config.RDSMASTERPASSWORD,\
                            port=3306,database="skike",\
                            cursorclass = pymysql.cursors.DictCursor)
    cursor = rdsDB.cursor()
    cursor.execute(sql)
    sql_all_return_user = cursor.fetchall()
    sql_tuple_list = []
    datenow = datetime.now()
    datenow_str = datenow.strftime("%Y-%m-%d %H:%M:%S")
    datenow_str_date = datenow.strftime("%Y-%m-%d")
    # print(datenow_str_yesterday, datenow_str_date)
    for user in sql_all_return_user:
        category_list = ["view", "view_item", "add_to_cart", "checkout"]
        category_result = numpy.random.choice(category_list, p=[0.73,0.17,0.06,0.04])
        category_result = str(category_result)
        if category_result == "view":
            for item in category_list[0:1]:
                sql_tuple = (datenow_str, user, item, datenow_str_date)
                sql_tuple_list.append(sql_tuple)
        elif category_result == "view_item":
            for item in category_list[0:2]:
                sql_tuple = (datenow_str, user, item, datenow_str_date)
                sql_tuple_list.append(sql_tuple)
        elif category_result == "add_to_cart":
            for item in category_list[0:3]:
                sql_tuple = (datenow_str, user, item, datenow_str_date)
                sql_tuple_list.append(sql_tuple)
        elif category_result == "checkout":
            for item in category_list[0:4]:
                sql_tuple = (datenow_str, user, item, datenow_str_date)
                sql_tuple_list.append(sql_tuple)
    try:
        sql_91_mock_data = "INSERT INTO stylish.data91app (`created_at`, `cid`, `category`, `date`)VALUES (%s, %s, %s, %s)"    
        cursor.executemany(sql_91_mock_data, sql_tuple_list)
        rds_DB.commit()
    except Exception as e:
        print("Exeception occured:{}".format(e))


def insert_data_for_91_dashboard():
    rds_DB = pymysql.connect(host=config.RDSHOSTNAME,\
                            user="admin",password=config.RDSMASTERPASSWORD,\
                            port=3306,database="stylish",\
                            cursorclass = pymysql.cursors.DictCursor)
    cursor = rds_DB.cursor()
    sql_tuple_list = []
    for number_mock_data in range(400):
        datenow = datetime.now()
        datenow_str = datenow.strftime("%Y-%m-%d %H:%M:%S")
        datenow_str_date = datenow.strftime("%Y-%m-%d")
        random_str_first = "".join(random.choice(string.ascii_lowercase + string.digits)for _ in range(8))
        random_str_second = "".join(random.choice(string.ascii_lowercase + string.digits)for _ in range(4))
        random_str_third = "".join(random.choice(string.ascii_lowercase + string.digits)for _ in range(4))
        random_str_fourth = "".join(random.choice(string.ascii_lowercase + string.digits)for _ in range(4))
        random_str_fiveth = "".join(random.choice(string.ascii_lowercase + string.digits)for _ in range(15))
        random_total = "{}-{}-{}-{}-{}".format(random_str_first,
                                            random_str_second,
                                            random_str_third,
                                            random_str_fourth,
                                            random_str_fiveth)
        category_list = ["view", "view_item", "add_to_cart", "checkout"]
        category_result = numpy.random.choice(category_list, p=[0.73,0.17,0.06,0.04])
        category_result = str(category_result)
        if category_result == "view":
            for item in category_list[0:1]:
                sql_tuple = (datenow_str, random_total, item, datenow_str_date)
                sql_tuple_list.append(sql_tuple)
        elif category_result == "view_item":
            for item in category_list[0:2]:
                sql_tuple = (datenow_str, random_total, item, datenow_str_date)
                sql_tuple_list.append(sql_tuple)
        elif category_result == "add_to_cart":
            for item in category_list[0:3]:
                sql_tuple = (datenow_str, random_total, item, datenow_str_date)
                sql_tuple_list.append(sql_tuple)
        elif category_result == "checkout":
            for item in category_list[0:4]:
                sql_tuple = (datenow_str, random_total, item, datenow_str_date)
                sql_tuple_list.append(sql_tuple)
    try:
        sql_91_mock_data = "INSERT INTO stylish.data91app (`created_at`, `cid`, `category`, `date`)VALUES (%s, %s, %s, %s)"    
        cursor.executemany(sql_91_mock_data, sql_tuple_list)
        rds_DB.commit()
        # print("now finish {} {} total will be {}".format())
    except Exception as e:
        print("Exeception occured:{}".format(e))


def total_run():
    for count in range(35):
        insert_data_for_91_dashboard()
        print("Total is 35 now is {}".format(count))



dashboard_task = PythonOperator(
    task_id='get_hotel_to_mongo_task',
    python_callable = total_run,
    dag = dag,
)

insert_return_id_task = PythonOperator(
    task_id='return_user',
    python_callable = insert_return_id,
    dag = dag,
)



insert_return_id_task >> dashboard_task