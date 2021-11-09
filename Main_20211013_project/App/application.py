from server import app
from waitress import serve
import pymysql
from server.models import product_model
from server.env import config

TABLES = config.TABLES

if __name__ == "__main__":
    if (app.env == "production"):
        serve(app, host='0.0.0.0', port = 3000)
    else:
        # rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
        #                         user="admin",password=config.RDSMASTERPASSWORD,\
        #                         port=3306,database="skike")
        # cursor = rdsDB.cursor()
        # product_model.create_tb_flight_ticket(cursor, TABLES=TABLES, TBNAME=config.TBNAME_FLYTICKET)
        # product_model.create_tb_stopover(cursor, TABLES=TABLES, TBNAME=config.TBNAME_STOPOVER)
        # product_model.create_tb_flightprice(cursor, TABLES=TABLES, TBNAME=config.TBNAME_FLIGHTPRICE)
        # product_model.create_tb_hotel(cursor, TABLES=TABLES, TBNAME=config.TBNAME_HOTEL)
        # product_model.create_tb_airport_geocode(cursor, TABLES=TABLES, TBNAME=config.TBNAME_FLIGHT_GEOCODE)
        # product_model.create_tb_hotel_alter(cursor, TABLES=TABLES, TBNAME=config.TBNAME_HOTEL_ALTER)
        # rdsDB.close()
        app.run('127.0.0.1', port = 5000)