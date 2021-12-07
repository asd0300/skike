from datetime import datetime, timedelta
import pymysql.cursors
from server.env import config
import jwt


def connect_skike_db():
    rds_db = pymysql.connect(
                            host=config.RDSHOSTNAME,
                            user="admin",
                            password=config.RDSMASTERPASSWORD,
                            port=config.RDSPORT,
                            database="skike",
                            cursorclass=pymysql.cursors.DictCursor)
    return rds_db


def connect_db(host, user, password, db_name=None, port=3306):
    """connect_db"""
    try:
        connect_db = pymysql.connect(host=host,
                                     port=port,
                                     user=user,
                                     password=password,
                                     database=db_name,)
        return connect_db
    except pymysql.MySQLError as e:
        print('Got error {!r}, errno is {}'.format(e, e.args[0]))
        return None


def create_db(cursor, DBNAME):
    """create_db"""
    # create database
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8mb4' "
            .format(DBNAME)
        )
    except Exception as e:
        print("Exeception occured:{}".format(e))

    # use database
    try:
        cursor.execute("USE {}".format(DBNAME))
    except Exception as e:
        print("Exeception occured:{}".format(e))

    return cursor


def create_tb_user(tables, tb_name=None):
    """create_tb_user"""
    tables[tb_name] = ("CREATE TABLE IF NOT EXISTS {}( \
        `email` varchar(255) NOT NULL,\
        `id` int NOT NULL AUTO_INCREMENT,\
        `provider` varchar(15) NOT NULL,\
        `password` varchar(255) NOT NULL,\
        `name` varchar(127) NOT NULL,\
        `picture` varchar(255) DEFAULT NULL,\
        `access_token` text NOT NULL,\
        `access_expired` bigint NOT NULL,\
        `login_at` timestamp NULL DEFAULT NULL,\
        PRIMARY KEY (`id`,`email`,`password`)\
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;".format(tb_name))


def create_tb_user_favorite(cursor, tables, tb_name=None):
    """create_tb_user_favorite"""
    tables[tb_name] = ("CREATE TABLE IF NOT EXISTS {}( \
        `id` int NOT NULL AUTO_INCREMENT,\
        `email` varchar(255) NOT NULL,\
        `want_time_start` varchar(255) DEFAULT NULL,\
        `want_time_end` varchar(255) DEFAULT NULL,\
        `hotel_name` varchar(255) DEFAULT NULL,\
        `hotel_img` varchar(255) DEFAULT NULL,\
        `hotel_detail` varchar(255) DEFAULT NULL,\
        `name` varchar(127) NOT NULL,\
        `location` varchar(255) DEFAULT NULL,\
        `price` int(10) DEFAULT NULL,\
        PRIMARY KEY (`id`,`email`)\
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;".format(tb_name))

    for table_name in tables:
        table_description = tables[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
            print("OK")
        except Exception as e:
            print("Exeception occured:{}".format(e))


def check_exist_user(email):
    """check_exist_user"""
    rds_db = connect_skike_db()
    cursor = rds_db.cursor()
    query = 'SELECT * FROM skike.user where email = "{}";'.format(str(email))
    cursor.execute(query)
    sign_up_data = cursor.fetchone()
    rds_db.commit()
    return sign_up_data


def insert_register_data(provider, name, email, hashed_password, picture,
                         acceess_expire):
    """insert_register_data"""
    rds_db = connect_skike_db()
    token_sign_up = jwt.encode({'provider': provider,
                                'name': name,
                                'email': email}, config.SECRET_KEY)
    try:
        sign_up_data = "INSERT INTO `user` (`provider`, `name`,\
                                    `email`, `password`, `picture`,\
                                    `access_token`, `access_expired`) \
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor = rds_db.cursor()
        cursor.execute(sign_up_data, (provider, name, email,
                                      hashed_password, picture,
                                      token_sign_up,
                                      acceess_expire))
        rds_db.commit()
    except Exception as e:
        print("Exeception occured:{}".format(e))


def insert_signin_data(email):
    """insert_signin_data"""
    rds_db = connect_skike_db()
    try:
        cursor = rds_db.cursor()
        query = 'SELECT * FROM skike.user WHERE email = "{}" ;'.format(email)
        cursor.execute(query)
        sign_data = cursor.fetchone()
        print(sign_data)
        rds_db.commit()
    except Exception as e:
        print("Exeception occured:{}".format(e))
    return sign_data

def get_user_page_data(conn,email):
    """get_user_page_data"""
    mydatabase = conn['skike_origin']
    mycollection = mydatabase['skike_favorite']
    pipeline = [
    {
        '$match': {
            'email': '{}'.format(email)
        }
    }
    ]
    result = mycollection.aggregate(pipeline)
    results = [doc for doc in result]
    print(results)
    return results
