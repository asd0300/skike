from flask import Flask
from pymongo import MongoClient
import pymysql,datetime
from datetime import timedelta

uri = "mongodb+srv://asd0300:*****@cluster0.w3mp9.mongodb.net/test?authSource=admin&replicaSet=atlas-bgr8kt-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true"
    
# Connect with the portnumber and host 
client = MongoClient(uri) 

mydatabase = client['skike_db'] 
# Access collection of the database 
mycollection=mydatabase['skike_collection'] 
# check collection exist?
mycollection.stats

