from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from env import config
import pymysql
from pymongo import MongoClient
###date generator
from datetime import date, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date' : days_ago(0,0,0,0,0),
    'email' : ['fan0300@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries' : 1,
    'retry_delay': timedelta(minutes =1)
}

dag = DAG(
    'test',
    default_args = default_args,
    description= 'Our first DAG with ETL process',
    schedule_interval = timedelta(days = 1)
)


def flight_data_insert():
    # print(Variable.get("varible"))
    print(config.PORT)

def flight_data_insert2():
    # print(Variable.get("secret_password"))
    print("ok")

flight_data_insert1 = PythonOperator(
    task_id='test1',
    python_callable = flight_data_insert,
    dag = dag,
)

hotel_data_insert2 = PythonOperator(
    task_id='test2',
    python_callable = flight_data_insert2,
    dag = dag,
)

flight_data_insert1 >> hotel_data_insert2