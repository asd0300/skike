import pymysql.cursors

# Connect to the database
import pymysql
from server import db


def connect_db(host, user, password, db_name=None, port=3306):
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
    # create database
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8mb4' ".format(DBNAME)
        )
    except Exception as e:
        print("Exeception occured:{}".format(e))

    # use database
    try:
        cursor.execute("USE {}".format(DBNAME))
    except Exception as e:
        print("Exeception occured:{}".format(e))

    return cursor

def create_tb_flight_ticket(cursor, TABLES, TBNAME=None):
    TABLES[TBNAME] = ("CREATE TABLE IF NOT EXISTS {}( \
        `id` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `depart_city` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `arrive_City` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `data_query_time` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `duration_min` INT(10) COLLATE utf8mb4_bin NOT NULL, \
        `depart_time` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `arrive_time` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `stopover_minutes` INT(10) COLLATE utf8mb4_bin NOT NULL, \
        `aircraft_registration` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `stayover_times` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `flight_company` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `category` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        PRIMARY KEY (`id`) \
        )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;".format(TBNAME))


def create_tb_stopover(cursor, TABLES, TBNAME=None):
    TABLES[TBNAME] = ("CREATE TABLE IF NOT EXISTS {}( \
        `id` INT(10) COLLATE utf8mb4_bin NOT NULL AUTO_INCREMENT, \
        `terminal_arrive_time` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `flight_depart_terminal` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `flight_arrive_terminal` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `flight_id` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        PRIMARY KEY (`id`), \
        FOREIGN KEY (`flight_id`) REFERENCES flight_ticket(id) \
        )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;".format(TBNAME))

def create_tb_flightprice(cursor, TABLES, TBNAME=None):
    TABLES[TBNAME] = ("CREATE TABLE IF NOT EXISTS {}( \
        `id` INT(10) COLLATE utf8mb4_bin NOT NULL AUTO_INCREMENT, \
        `product_flag` INT(10) COLLATE utf8mb4_bin NOT NULL, \
        `price` INT(10) COLLATE utf8mb4_bin NOT NULL, \
        `adult_price` varchar(200) COLLATE utf8mb4_bin NULL, \
        `child_price` varchar(200) COLLATE utf8mb4_bin NULL, \
        `flight_class` varchar(200) COLLATE utf8mb4_bin NOT NULL, \
        `available_tickets` INT(10) COLLATE utf8mb4_bin NOT NULL, \
        `flight_ticket_feature` varchar(200) COLLATE utf8mb4_bin NOT NULL, \
        `flight_category` varchar(200) COLLATE utf8mb4_bin NOT NULL, \
        `ticket_description` varchar(200) COLLATE utf8mb4_bin NOT NULL, \
        `flight_id` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        PRIMARY KEY (`id`), \
        FOREIGN KEY (`flight_id`) REFERENCES flight_ticket(id) \
        )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;".format(TBNAME))

# def create_tb_flightpriceChild(cursor, TABLES, TBNAME=None):
#     TABLES[TBNAME] = ("CREATE TABLE IF NOT EXISTS {}( \
#         `id` INT(10) COLLATE utf8mb4_bin NOT NULL AUTO_INCREMENT, \
#         `productFlag` INT(10) COLLATE utf8mb4_bin NOT NULL, \
#         `viewTotalPrice` INT(10) COLLATE utf8mb4_bin NOT NULL, \
#         `childPrice` varchar(200) COLLATE utf8mb4_bin NOT NULL, \
#         `productClass` varchar(200) COLLATE utf8mb4_bin NOT NULL, \
#         `availableTickets` INT(10) COLLATE utf8mb4_bin NOT NULL, \
#         `productName` varchar(200) COLLATE utf8mb4_bin NOT NULL, \
#         `productCategory` varchar(200) COLLATE utf8mb4_bin NOT NULL, \
#         `ticketDescription` varchar(200) COLLATE utf8mb4_bin NOT NULL, \
#         `product_id` INT(10) COLLATE utf8mb4_bin NOT NULL, \
#         PRIMARY KEY (`id`), \
#         FOREIGN KEY (`product_id`) REFERENCES flyticket(id) \
#         )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;".format(TBNAME))

def create_tb_airport_geocode(cursor, TABLES, TBNAME=None):
    TABLES[TBNAME] = ("CREATE TABLE IF NOT EXISTS {}( \
        `airport_name` varchar(200) COLLATE utf8mb4_bin NOT NULL, \
        `geocode_lat` float(10) COLLATE utf8mb4_bin NOT NULL, \
        `geocode_lng` float(10) COLLATE utf8mb4_bin NOT NULL, \
        PRIMARY KEY (`airport_name`) \
        )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;".format(TBNAME))

def create_tb_hotel(cursor, TABLES, TBNAME=None):
    TABLES[TBNAME] = ("CREATE TABLE IF NOT EXISTS {}( \
        `id` INT(10) COLLATE utf8mb4_bin NOT NULL, \
        `data_query_time` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `name` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `hotel_near_location` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `hotel_near_location_meter` INT(10) COLLATE utf8mb4_bin NOT NULL, \
        `hotel_rating_count` INT(10) COLLATE utf8mb4_bin NOT NULL, \
        `hotel_rating_avg_score` float(10) COLLATE utf8mb4_bin NOT NULL, \
        `hotel_best_price_per_stay` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `category` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `locality` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `image_url` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `geocode_lat` float(10) COLLATE utf8mb4_bin NOT NULL, \
        `geocode_lng` float(10) COLLATE utf8mb4_bin NOT NULL, \
        PRIMARY KEY (`id`, `data_query_time`) \
        )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;".format(TBNAME))


def create_tb_hotel_alter(cursor, TABLES, TBNAME=None):
    TABLES[TBNAME] = ("CREATE TABLE IF NOT EXISTS {}( \
        `id` INT(10) COLLATE utf8mb4_bin NOT NULL AUTO_INCREMENT, \
        `data_query_time` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `hotel_agency` varchar(255) COLLATE utf8mb4_bin NOT NULL,    \
        `agency_logo` varchar(255) COLLATE utf8mb4_bin NOT NULL,    \
        `hotel_feature` varchar(255) COLLATE utf8mb4_bin NOT NULL, \
        `price` INT(10) COLLATE utf8mb4_bin NOT NULL, \
        `hotel_url` Text COLLATE utf8mb4_bin  NULL, \
        `hotel_id` INT(10) COLLATE utf8mb4_bin NOT NULL, \
        PRIMARY KEY (`id`,`hotel_feature`,`price`), \
        FOREIGN KEY (`hotel_id`,`data_query_time`) REFERENCES hotel(`id`,`data_query_time`) \
        )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;".format(TBNAME))
    
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
            print("OK")
        except Exception as e:
            print("Exeception occured:{}".format(e))

def get_products(page_size, paging, requirement = {}):
    pass
#     product_query = None
#     if ("category" in requirement):
#         category = requirement.get("category")
#         if (category == 'all'):
#             product_query = Flyticket.query.filter_by(source = 'native')
#         else:
#             product_query = Flyticket.query.filter_by(source = 'native', category = category)
#     elif ("keyword" in requirement):
#         # q = Flyticket.join(subq, subq.c.id == Address.user_id)
#         # Comment_alias = aliased(Comment, name='comment_alias') db.session.query(User.id, User.username, User.email, User.phone, Comment.comment).join(Comment, Comment.user_id == User.id).join(Comment_alias, Comment_alias.user_id == User.id).all() 原文網址：https://itw01.com/8JAS5EY.html
#         product_query = Flyticket.query.filter_by(source = 'native').filter(Flyticket.title.like(f"%{requirement.get('keyword')}%"))
#     elif ("id" in requirement):
#         product_query = Flyticket.query.filter_by(id = requirement.get("id"))
#     elif ("source" in requirement):
#         product_query = Flyticket.query.filter_by(source = requirement.get("source"))

        
#     products = product_query.limit(page_size).offset(page_size * paging).all()
# #     count = product_query.count()
# #     return {
# #         "products": [p.to_json() for p in products],
# #         "product_count": count
# #     }

# # def get_airTicket(page_size, paging, requirement = {}):
# #     product_query = None
# #     if ("category" in requirement):
# #         category = requirement.get("category")
# #         if (category == 'all'):
# #             product_query = Product.query.filter_by(source = 'native')
# #         else:
# #             product_query = Product.query.filter_by(source = 'native', category = category)
# #     elif ("keyword" in requirement):
# #         product_query = Product.query.filter_by(source = 'native').filter(Product.title.like(f"%{requirement.get('keyword')}%"))
# #     elif ("id" in requirement):
# #         product_query = Product.query.filter_by(id = requirement.get("id"))
# #     elif ("source" in requirement):
# #         product_query = Product.query.filter_by(source = requirement.get("source"))
# #     elif ("recommend" in requirement):
# #         product_query = Product.query.join(SimilarityModel, Product.id == SimilarityModel.item2_id)\
# #             .filter_by(item1_id = requirement.get("recommend"))\
# #             .order_by(SimilarityModel.similarity.desc())
        
# #     products = product_query.limit(page_size).offset(page_size * paging).all()
# #     count = product_query.count()
# #     return {
# #         "products": [p.to_json() for p in products],
# #         "product_count": count
# #     }


def get_products_variants(product_ids):
    pass
# #     variants = Variant.query.filter(Product.id.in_(product_ids)).all()
# #     return [v.to_json() for v in variants]

# def create_product(product, variants):
# def create_product(flyticket,stopover, flightprice):
#     try:
#         flyticket_model = Flyticket(**flyticket)
#         db.session.add(flyticket_model)
#         db.session.flush()

#         db.session.bulk_insert_mappings(
#             Stopover,
#             stopover
#         )
#         db.session.bulk_insert_mappings(
#             Flightprice,
#             flightprice
#         )
#         db.session.commit()
#     except Exception as e:
#         print(e)

# def create_product_child(flyticket,stopover, flightpriceChild):
#     try:
#         flyticket_model = Flyticket(**flyticket)
#         db.session.add(flyticket_model)
#         db.session.flush()

#         db.session.bulk_insert_mappings(
#             Stopover,
#             stopover
#         )
#         db.session.bulk_insert_mappings(
#             FlightpriceChild,
#             flightpriceChild
#         )
#         db.session.commit()
#     except Exception as e:
#         print(e)