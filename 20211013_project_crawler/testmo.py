from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import time,re
import requests
import json,random
from pymongo import MongoClient
import concurrent.futures
from env import config
###date generator
from datetime import  datetime,timedelta,date
import pymysql
import urllib.parse
def insert_hotel_mongo_to_RDS():
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

insert_hotel_mongo_to_RDS