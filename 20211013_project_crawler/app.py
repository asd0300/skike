from server import app
from waitress import serve
from flask import render_template
from env import config
import imghdr, datetime
from flask_sqlalchemy import SQLAlchemy
import redis
redis.client = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)







TODAY = datetime.datetime.today().strftime('%Y-%m-%d')

# sever var
DEBUG = config.DEBUG
PORT = config.PORT
HOST = config.HOST
SECRET_KEY = config.SECRET_KEY

# db var
DBHOST = config.DBHOST
DBUSER = config.DBUSER
DBPASSWORD = config.DBPASSWORD
DBNAME = config.DBNAME
TABLES = config.TABLES
TBNAME_PRODUCTS = config.TBNAME_PRODUCTS
TBNAME_COLORS = config.TBNAME_COLORS
TBNAME_VARIANTS = config.TBNAME_VARIANTS
TBNAME_USER = config.TBNAME_USER
TBNAME_MAIN_IMAGE = config.TBNAME_MAIN_IMAGE
TBNAME_OTHER_IMAGES = config.TBNAME_OTHER_IMAGES
TBNAME_MONGO91DATA = config.TBNAME_MONGO91DATA
TBNAME_MONGO91MEMBER = config.TBNAME_MONGO91MEMBER

# STATIC_FOLDER = 'static'
# app = Flask(__name__,static_folder=STATIC_FOLDER)

##


# app.config['MAX_CONTENT_LENGTH'] = 1024
# app.config.from_object(config)
# app.config['JSON_AS_ASCII'] = False
# app.config['JSON_SORT_KEYS'] = False



@app.route('/')
@app.route('/main_skike.html', methods=['GET'])
def admin_product():
    return render_template('product.html')




# @app.route('/', methods = ['GET', 'POST'])
# def index():
#     """home"""
#     paging = request.args.get('paging', 0, type=int)
#     tag = request.args.get('tag', 'all')
#     apiUrl='http://localhost:8080/api/1.0/products/{}{}{}'.format(tag,'?paging=',paging)
#     with urllib.request.urlopen(apiUrl) as url:
#         urlData = url.read().decode()
#         data=json.loads(urlData)
#     nextPage=data['next_paging'] if 'next_paging' in data else None
#     return render_template('main.html', data = data , nextPage = nextPage)




# @app.route('/api/1.0/products/all', methods=['get'])
# def all():
#     """all proc"""
#     paging = request.args.get('paging')
#     if paging == None or paging == '':
#         paging = 0
#     rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
#                             user="admin",password=config.RDSMASTERPASSWORD,\
#                             port=3306,database="stylish")
#     cursor = rdsDB.cursor()
#     sql = "SELECT * FROM stylish.cloth_product LIMIT {},{}".\
#         format(str(int(paging)*6),6)
#     # sql = "SELECT * FROM stylish.products where category LIKE '男%' LIMIT 1;"
#     cursor.execute(sql)
#     u = cursor.fetchall()
#     productList = []
#     for result in u:
#         colorList = []
#         variantList = []
#         imagesList = []
#         sizeList = []
#         productContent = {'id':result[0], 'title':result[2], 'description':result[3],\
#                           'price':result[4], 'texture':result[5],\
#                           'wash':result[6], 'place':result[7], \
#                           'note':result[8], 'story':result[9]}

#         sqlColor = "SELECT * FROM stylish.colors"
#         cursor.execute(sqlColor)
#         uColor = cursor.fetchall()
#         for resultColor in uColor:
#             if result[0] == resultColor[1]:
#                 colorContent = {'name':resultColor[2], 'code':resultColor[3]}
#                 colorList.append(colorContent)
#                 colorContent = {}
#             colorDict = dict(colors = colorList)
#             cursor.close

#         sqlVariant = "SELECT * FROM stylish.variants;"
#         cursor.execute(sqlVariant)
#         uVariant = cursor.fetchall()
#         for resultVariant in uVariant:
#             if result[0] == resultVariant[1]:
#                 variantContent = {'color_code':resultVariant[2],\
#                                   'size':resultVariant[3],\
#                                   'stock':resultVariant[4]}
#                 sizeContent = resultVariant[3]
#                 sizeList.append(sizeContent)
#                 variantList.append(variantContent)
#                 variantContent = {}
#             sizeDict = dict(sizes = sizeList)
#             variantDict = dict(variants = variantList)
#             cursor.close
#         sqlImages = "SELECT * FROM stylish.other_images;"
#         cursor.execute(sqlImages)
#         uImages = cursor.fetchall()
#         for resultImages in uImages:
#             if result[0] == resultImages[1]:
#                 imagesContent = resultImages[2]
#                 imagesList.append(imagesContent)
#                 d = dict(images = imagesList)
#                 imagesContent = {}
#             cursor.close
#         colorDict.update(sizeDict)
#         colorDict.update(variantDict)
#         mainImageContent = {'main_image':result[13]}
#         mainImageContent.update(d)
#         colorDict.update(mainImageContent)
#         productContent.update(colorDict)
#         productList.append(productContent)
#     a = dict(data = productList)
#     sqlNext = "SELECT * FROM stylish.cloth_product LIMIT {},{}".\
#         format(str((int(paging)+1)*6),str(6))
#     cursor.execute(sqlNext)
#     uNext = cursor.fetchall()
#     if uNext:
#         a["next_paging"] =(int(paging)+1)
#     cursor.close
#     return jsonify(a)


# @app.route('/api/1.0/products/men', methods=['get'])
# def men():
#     """men part"""
#     paging = request.args.get('paging')
#     if paging == None or paging == '':
#         paging = 0
#     rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
#                             user="admin",password=config.RDSMASTERPASSWORD,\
#                             port=3306,database="stylish")
#     cursor = rdsDB.cursor()
#     sql = "SELECT * FROM stylish.cloth_product where category LIKE '男%' LIMIT {},{}".\
#         format(str(int(paging)*6),6)
#     # sql = "SELECT * FROM stylish.products where category LIKE '男%' LIMIT 1;"
#     cursor.execute(sql)
#     u = cursor.fetchall()
#     productList = []
#     for result in u:
#         colorList = []
#         variantList = []
#         imagesList = []
#         sizeList = []
#         productContent = {'id':result[0], 'title':result[2],\
#                           'description':result[3],\
#                           'price':result[4], 'texture':result[5],\
#                           'wash':result[6], 'place':result[7], \
#                           'note':result[8], 'story':result[9]}

#         sqlColor = "SELECT * FROM stylish.colors"
#         cursor.execute(sqlColor)
#         uColor = cursor.fetchall()
#         for resultColor in uColor:
#             if result[0] == resultColor[1]:
#                 colorContent = {'name':resultColor[2], 'code':resultColor[3]}
#                 colorList.append(colorContent)
#                 colorContent = {}
#             colorDict = dict(colors = colorList)
#             cursor.close

#         sqlVariant = "SELECT * FROM stylish.variants;"
#         cursor.execute(sqlVariant)
#         uVariant = cursor.fetchall()
#         for resultVariant in uVariant:
#             if result[0] == resultVariant[1]:
#                 variantContent = {'color_code':resultVariant[2],\
#                     'size':resultVariant[3],\
#                     'stock':resultVariant[4]}
#                 sizeContent = resultVariant[3]
#                 sizeList.append(sizeContent)
#                 variantList.append(variantContent)
#                 variantContent = {}
#             sizeDict = dict(sizes = sizeList)
#             variantDict = dict(variants = variantList)
#             cursor.close

#         sqlImages = "SELECT * FROM stylish.other_images;"
#         cursor.execute(sqlImages)
#         uImages = cursor.fetchall()
#         for resultImages in uImages:
#             if result[0] == resultImages[1]:
#                 imagesContent = resultImages[2]
#                 imagesList.append(imagesContent)
#                 d = dict(images = imagesList)
#                 imagesContent = {}

#             cursor.close
#         colorDict.update(sizeDict)
#         colorDict.update(variantDict)
#         mainImageContent = {'main_image':result[13]}
#         mainImageContent.update(d)
#         colorDict.update(mainImageContent)
#         productContent.update(colorDict)
#         productList.append(productContent)
#     a = dict(data = productList)
#     sqlNext = "SELECT * FROM stylish.cloth_product where category LIKE '男%' LIMIT {},{}".\
#         format(str((int(paging)+1)*6),str(6))
#     cursor.execute(sqlNext)
#     uNext = cursor.fetchall()
#     if uNext:
#         a["next_paging"] =(int(paging)+1)
#     cursor.close
#     return jsonify(a)
# @app.route('/api/1.0/products/women', methods=['get'])
# def women():
#     """women part"""
#     paging = request.args.get('paging')
#     if paging == None or paging == '':
#         paging = 0
#     rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
#                             user="admin",password=config.RDSMASTERPASSWORD,\
#                             port=3306,database="stylish")
#     cursor = rdsDB.cursor()
#     sql = "SELECT * FROM stylish.cloth_product where category LIKE '女%' LIMIT {},{}".\
#         format(str(int(paging)*6),6)
#     cursor.execute(sql)
#     u = cursor.fetchall()
#     productList = []
#     for result in u:
#         colorList = []
#         variantList = []
#         imagesList = []
#         sizeList = []
#         productContent = {'id':result[0], 'title':result[2],\
#                           'description':result[3],\
#                           'price':result[4],\
#                           'texture':result[5],\
#                           'wash':result[6],\
#                           'place':result[7], \
#                           'note':result[8],\
#                           'story':result[9]}

#         sqlColor = "SELECT * FROM stylish.colors"
#         cursor.execute(sqlColor)
#         uColor = cursor.fetchall()
#         for resultColor in uColor:
#             if result[0] == resultColor[1]:
#                 colorContent = {'name':resultColor[2], 'code':resultColor[3]}
#                 colorList.append(colorContent)
#                 colorContent = {}
#             colorDict = dict(colors = colorList)
#             cursor.close

#         sqlVariant = "SELECT * FROM stylish.variants;"
#         cursor.execute(sqlVariant)
#         uVariant = cursor.fetchall()
#         for resultVariant in uVariant:
#             if result[0] == resultVariant[1]:
#                 variantContent = {'color_code':resultVariant[2],\
#                                   'size':resultVariant[3],\
#                                   'stock':resultVariant[4]}
#                 sizeContent = resultVariant[3]
#                 sizeList.append(sizeContent)
#                 variantList.append(variantContent)
#                 variantContent = {}
#             sizeDict = dict(sizes = sizeList)
#             variantDict = dict(variants = variantList)
#             cursor.close

#         sqlImages = "SELECT * FROM stylish.other_images;"
#         cursor.execute(sqlImages)
#         uImages = cursor.fetchall()
#         for resultImages in uImages:
#             if result[0] == resultImages[1]:
#                 imagesContent = resultImages[2]
#                 imagesList.append(imagesContent)
#                 d = dict(images = imagesList)
#                 imagesContent = {}

#             cursor.close
#         colorDict.update(sizeDict)
#         colorDict.update(variantDict)
#         mainImageContent = {'main_image':result[13]}
#         mainImageContent.update(d)
#         colorDict.update(mainImageContent)
#         productContent.update(colorDict)
#         productList.append(productContent)
#     a = dict(data = productList)
#     sqlNext = "SELECT * FROM stylish.cloth_product where category LIKE '女%' LIMIT {},{}".\
#         format(str((int(paging)+1)*6),str(6))
#     cursor.execute(sqlNext)
#     uNext = cursor.fetchall()
#     if uNext:
#         a["next_paging"] =(int(paging)+1)
#     cursor.close
#     return jsonify(a)

# @app.route('/api/1.0/products/accessories', methods=['get'])
# def accessories():
#     """accesories"""
#     paging = request.args.get('paging')
#     if paging == None or paging == '':
#         paging = 0
#     rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
#                             user="admin",password=config.RDSMASTERPASSWORD,\
#                             port=3306,database="stylish")
#     cursor = rdsDB.cursor()
#     sql = "SELECT * FROM stylish.cloth_product where category LIKE '飾%' LIMIT {},{}".\
#         format(str(int(paging)*6),6)
#     cursor.execute(sql)
#     u = cursor.fetchall()
#     productList = []
#     for result in u:
#         colorList = []
#         variantList = []
#         imagesList = []
#         sizeList = []
#         productContent = {'id':result[0], 'title':result[2],\
#                           'description':result[3],\
#                           'price':result[4],\
#                           'texture':result[5],\
#                           'wash':result[6],\
#                           'place':result[7], \
#                           'note':result[8],\
#                           'story':result[9]}

#         sqlColor = "SELECT * FROM stylish.colors"
#         cursor.execute(sqlColor)
#         uColor = cursor.fetchall()
#         for resultColor in uColor:
#             if result[0] == resultColor[1]:
#                 colorContent = {'name':resultColor[2], 'code':resultColor[3]}
#                 colorList.append(colorContent)
#                 colorContent = {}
#             colorDict = dict(colors = colorList)
#             cursor.close

#         sqlVariant = "SELECT * FROM stylish.variants;"
#         cursor.execute(sqlVariant)
#         uVariant = cursor.fetchall()
#         for resultVariant in uVariant:
#             if result[0] == resultVariant[1]:
#                 variantContent = {'color_code':resultVariant[2],\
#                                   'size':resultVariant[3],\
#                                   'stock':resultVariant[4]}
#                 sizeContent = resultVariant[3]
#                 sizeList.append(sizeContent)
#                 variantList.append(variantContent)
#                 variantContent = {}
#             sizeDict = dict(sizes = sizeList)
#             variantDict = dict(variants = variantList)
#             cursor.close

#         sqlImages = "SELECT * FROM stylish.other_images;"
#         cursor.execute(sqlImages)
#         uImages = cursor.fetchall()
#         for resultImages in uImages:
#             if result[0] == resultImages[1]:
#                 imagesContent = resultImages[2]
#                 imagesList.append(imagesContent)
#                 d = dict(images = imagesList)
#                 imagesContent = {}

#             cursor.close
#         colorDict.update(sizeDict)
#         colorDict.update(variantDict)
#         mainImageContent = {'main_image':result[13]}
#         mainImageContent.update(d)
#         colorDict.update(mainImageContent)
#         productContent.update(colorDict)
#         productList.append(productContent)
#     a = dict(data = productList)
#     sqlNext = "SELECT * FROM stylish.cloth_product where category LIKE '飾%' LIMIT {},{}".\
#         format(str((int(paging)+1)*6),str(6))
#     cursor.execute(sqlNext)
#     uNext = cursor.fetchall()
#     if uNext:
#         a["next_paging"] =(int(paging)+1)
#     cursor.close
#     return jsonify(a)


# @app.route('/api/1.0/products/search', methods=['get'])
# def search():
#     """product search"""
#     keyword = request.args.get('keyword')
#     paging = request.args.get('paging', default=0, type=int)
#     rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
#                             user="admin",password=config.RDSMASTERPASSWORD,\
#                             port=3306,database="stylish")
#     cursor = rdsDB.cursor()
#     sql = "SELECT * FROM stylish.cloth_product where title  LIKE\
#           '{}%' or title  LIKE '%{}' or   title  LIKE '%{}%' \
#           LIMIT {},{};".\
#           format(keyword,keyword,keyword,str(int(paging)*6),str(6))
#     cursor.execute(sql)
#     uSearch = cursor.fetchall()
#     searchList = []
#     for result in uSearch:
#         colorList = []
#         variantList = []
#         imagesList = []
#         sizeList = []
#         searchContent= {'id':result[0], 'category':result[1],\
#                         'title':result[2], 'description':result[3],\
#                         'price':result[4], 'texture':result[5],\
#                         'wash':result[6], 'place':result[7],\
#                         'note':result[8], 'story':result[9],\
#                         'main_image':result[13]}

#         sqlColor = "SELECT * FROM stylish.colors"
#         cursor.execute(sqlColor)
#         uColor = cursor.fetchall()
#         for resultColor in uColor:
#             if result[0] == resultColor[1]:
#                 colorContent = {'name':resultColor[2], 'code':resultColor[3]}
#                 colorList.append(colorContent)
#                 colorContent = {}
#             colorDict = dict(colors = colorList)
#             cursor.close
#         sqlVariant = "SELECT * FROM stylish.variants;"
#         cursor.execute(sqlVariant)
#         uVariant = cursor.fetchall()
#         for resultVariant in uVariant:
#             if result[0] == resultVariant[1]:
#                 variantContent = {'color_code':resultVariant[2],\
#                                   'size':resultVariant[3],\
#                                   'stock':resultVariant[4]}
#                 sizeContent = resultVariant[3]
#                 sizeList.append(sizeContent)
#                 variantList.append(variantContent)
#                 variantContent = {}
#             sizeDict = dict(sizes = sizeList)
#             variantDict = dict(variants = variantList)
#             cursor.close
#         sqlImages = "SELECT * FROM stylish.other_images;"
#         cursor.execute(sqlImages)
#         uImages = cursor.fetchall()
#         for resultImages in uImages:
#             if result[0] == resultImages[1]:
#                 imagesContent = resultImages[2]
#                 imagesList.append(imagesContent)
#                 d = dict(images = imagesList)
#                 imagesContent = {}

#             cursor.close
#         d.update(variantDict)
#         d.update(colorDict)
#         d.update(sizeDict)
#         searchContent.update(d)
#         searchList.append(searchContent)
#     a = dict(data = searchList)
#     sqlNext = "SELECT * FROM stylish.cloth_product where title  LIKE '{}%' or\
#     title  LIKE '%{}' or   title  LIKE '%{}%' LIMIT {},{};"\
#     .format(keyword,keyword,keyword,str((int(paging)+1)*6),str(6))
#     cursor.execute(sqlNext)
#     uNext = cursor.fetchall()
#     if uNext:
#         a["next_paging"] =(int(paging)+1)
#     cursor.close
#     return jsonify(a)


# @app.route('/api/1.0/products/details', methods=['get'])
# def details():
#     """details"""
#     id = request.args.get('id')
#     rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
#                             user="admin",password=config.RDSMASTERPASSWORD,\
#                             port=3306,database="stylish")
#     cursor = rdsDB.cursor()
#     sql = "SELECT * FROM stylish.cloth_product where id  ='{}' ".format(id)
#     cursor.execute(sql)
#     uSearch = cursor.fetchall()
#     # productList = []
#     for result in uSearch:
#         colorList = []
#         variantList = []
#         imagesList = []
#         sizeList = []
#         productContent = {'id':result[0], 'title':result[2],\
#                           'description':result[3],\
#                           'price':result[4], 'texture':result[5],\
#                           'wash':result[6], 'place':result[7], \
#                           'note':result[8], 'story':result[9]}

#         sqlColor = "SELECT * FROM stylish.colors"
#         cursor.execute(sqlColor)
#         uColor = cursor.fetchall()
#         for resultColor in uColor:
#             if result[0] == resultColor[1]:
#                 colorContent = {'name':resultColor[2], 'code':resultColor[3]}
#                 colorList.append(colorContent)
#                 colorContent = {}
#             colorDict = dict(colors = colorList)
#             cursor.close
#         sqlVariant = "SELECT * FROM stylish.variants;"
#         cursor.execute(sqlVariant)
#         uVariant = cursor.fetchall()
#         for resultVariant in uVariant:
#             if result[0] == resultVariant[1]:
#                 variantContent = {'color_code':resultVariant[2],\
#                                   'size':resultVariant[3],\
#                                   'stock':resultVariant[4]}
#                 sizeContent = resultVariant[3]
#                 sizeList.append(sizeContent)
#                 variantList.append(variantContent)
#                 variantContent = {}
#             sizeDict = dict(sizes = sizeList)
#             variantDict = dict(variants = variantList)
#             cursor.close

#         sqlImages = "SELECT * FROM stylish.other_images;"
#         cursor.execute(sqlImages)
#         uImages = cursor.fetchall()
#         for resultImages in uImages:
#             if result[0] == resultImages[1]:
#                 imagesContent = resultImages[2]
#                 imagesList.append(imagesContent)
#                 d = dict(images = imagesList)
#                 imagesContent = {}

#             cursor.close
#         colorDict.update(sizeDict)
#         colorDict.update(variantDict)
#         mainImageContent = {'main_image':result[13]}
#         mainImageContent.update(d)
#         colorDict.update(mainImageContent)
#         productContent.update(colorDict)
#     detailFinal = {"data":productContent}
#     return jsonify(detailFinal)

# @app.route('/api/1.0/user/signup', methods=['post'])
# def register():
#     """register"""
#     if request.method == 'POST' :
#         userDetails = request.json
#         name = userDetails['name']
#         email = userDetails['email']
#         password = userDetails['password']
#         provider = "native"
#         hashed_password = generate_password_hash(password)
#         acceess_expire = 86400
#         tokenSignUp = jwt.encode({'provider':provider,\
#                                   'name':name,\
#                                   'email': email ,\
#                                   'picture':""}, SECRET_KEY)
#         # tokenAfterDecode=tokenSignUp.decode('utf8').replace("'", '"')
#         # tokenAfterDecode=tokenSignUp.decode('utf8').replace("'", '"')
#         rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
#                             user="admin",password=config.RDSMASTERPASSWORD,\
#                             port=3306,database="stylish")
#         cursor = rdsDB.cursor()
#         models.create_tb_user(cursor, TABLES=TABLES, TBNAME=TBNAME_USER)
#         query = 'SELECT * FROM stylish.user where email = "{}";'.format(str(email))
#         cursor.execute(query)
#         signUpData = cursor.fetchone()
#         rdsDB.commit()
#         picture =""
#         if signUpData:
#             error = "A person with this email or name already exists, please try another email name"
#             rdsDB.close()
#             flash(error)
#         else:
#             if provider =="native":
#                 sqlSignUp = "INSERT INTO `user` (`provider`, `name`,\
#                              `email`, `password`, `picture`,\
#                              `access_token`, `access_expired`) \
#                              VALUES (%s, %s, %s, %s, %s, %s, %s)"
#                 cursor.execute(sqlSignUp, (provider, name, email,\
#                                hashed_password, picture, tokenSignUp,\
#                                acceess_expire))
#                 rdsDB.commit()
#                 query = 'SELECT * FROM stylish.user where email = "{}";'.format(str(email))
#                 cursor.execute(query)
#                 signUpAfter=cursor.fetchone()
#                 print(signUpAfter[0])
#                 provider = "native"
#                 # token_Json =signUpAfter[6].decode('utf8').replace("'", '"')
#                 userAccess = {'access_token':signUpAfter[6], 'access_expired':signUpAfter[7]}
#                 # userAccess = {}
#                 userContent = {"id":signUpAfter[0],"provider":signUpAfter[1],\
#                                 "name":signUpAfter[2], "email":signUpAfter[3],\
#                                 "picture":signUpAfter[5]}
#                 rdsDB.commit()
#                 error = "Register Success!"
#                 tempA={"user":userContent}
#                 userAccess.update(tempA)
#             finalSignup = {"data":userAccess}
#         rdsDB.close()
#         return jsonify(finalSignup)


# @app.route('/api/1.0/user/signin', methods=['post'])
# def login():
#     """login"""
#     if request.method == 'POST' :
#         userDetails = request.json
#         email = userDetails['email']
#         provider = userDetails['provider']
#         if provider == "native":
#             connectDB = models.connect_db(DBHOST, DBUSER, DBPASSWORD,db_name = 'stylish')
#             cursor = connectDB.cursor()
#             query = 'SELECT * FROM user WHERE email = "{}" ;'.format(email)
#             cursor.execute(query)
#             signdata = cursor.fetchone()
#             connectDB.commit()
#             if signdata:
#                 signContent = {'access_token':signdata[6], 'access_expired':signdata[7]}
#                 userContent = {'id': signdata[0],"provider": signdata[1],\
#                     "name": signdata[2],"email": signdata[3],\
#                     "picture": signdata[5]}
#                 userTemp = {"user":userContent}
#                 signContent.update(userTemp)
#                 signdataFinal = {"data":signContent}
#                 connectDB.close()

#                 return jsonify(signdataFinal)
#     return make_response('Could not verify', 403)

# @app.route('/api/1.0/user/profile', methods=['GET'])
# def userProfile():
#     """profile"""
#     headers = request.headers# 抓header
#     if 'Authorization' in headers:
#         requestToken = headers['Authorization'].replace('Bearer ', '')
#         detoken = jwt.decode(requestToken, SECRET_KEY, algorithms=["HS256"])
#         profileFinal= {"data":detoken}
#         return profileFinal



# @app.route('/dashboard', methods=["get","post"])
# def dashboard():
#     """dashboard"""
#     rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
#                             user="admin",password=config.RDSMASTERPASSWORD,\
#                             port=3306,database="stylish",
#                             cursorclass = pymysql.cursors.DictCursor)
#     cursor = rdsDB.cursor()
#     models.create_tb_mongo91Data(cursor, TABLES=TABLES, TBNAME=TBNAME_MONGO91DATA)
#     models.create_tb_mongo91Member(cursor, TABLES=TABLES, TBNAME=TBNAME_MONGO91MEMBER)
#     mongoPipeline.dashboardgetSQL(cursor, rdsDB)
#     endDate = request.values.get('endDate')
#     if  not endDate:
#         startDate = datetime.datetime.today().strftime('%Y-%m-%d')
#         endDate = datetime.datetime.today()+timedelta(days=1)
#         endDate = endDate.strftime('%Y-%m-%d')
#     else:
#         startDate = endDate

#         endDate = datetime.datetime.strptime(endDate,"%Y-%m-%d")
#         endDate = endDate+timedelta(days=1)
#         endDate = endDate.strftime('%Y-%m-%d')
#     print("sql done")
#     funnel = mongoPipeline.data_output_funnel(cursor, startDate, endDate)
#     print("funnel done")
#     active = mongoPipeline.count_daily_active(cursor, startDate, endDate)
#     print("active done")
#     endDate = datetime.datetime.strptime(endDate,"%Y-%m-%d")
#     endDate = endDate+timedelta(days=-1)
#     endDate = endDate.strftime('%Y-%m-%d')
#     startDate = datetime.datetime.strptime(startDate,"%Y-%m-%d")
#     startDate = startDate+timedelta(days=-1)
#     startDate = startDate.strftime('%Y-%m-%d')
#     count = mongoPipeline.count_all_user(cursor, endDate)
#     print("count done")




#     return render_template('user91.html',
#                             ttl_counts = count,
#                             startDate=startDate,
#                             endDate=endDate,
#                             data1=funnel[0],
#                             data2=funnel[1],
#                             data3=funnel[2],
#                             data4=funnel[3],
#                             data5=active[0],
#                             data6=active[1],
#                             data7=active[2])




# @app.route('/recommandation')
# def recommandation(product=None):
#     """recommandation table"""
#     product = request.args.get('product', product)
#     redisData = redis.client.hgetall('recommand')
#     if len(redisData) ==0:
#         sqlQuery = 'SELECT title1, imgurl1, pid2, title2, imgurl2,\
#             pid1 FROM stylish.product_final group by pid2 having title2 !="None";'
#         rdsDB = pymysql.connect(host=config.RDSHOSTNAME,\
#                             user="admin",password=config.RDSMASTERPASSWORD,\
#                             port=3306,database="stylish")
#         cursor = rdsDB.cursor()
#         cursor.execute(sqlQuery)
#         things = [{'title1': row[0], 'imgurl1': row[1], 'pid2': row[2],\
#             'title2': row[3], 'imgurl2': row[4], 'pid1': row[5]} for row in cursor.fetchall()]
#         key =1
#         for data in things:
#             value = json.dumps(data)
#             redis.client.hset('recommand',key,value)
#             key += 1
#         redisData = redis.client.hgetall('recommand')
#         redis.client.expire('recommand', 60)
#     productList = []
#     recomList = []
#     if product is None:
#         for key, data in redisData.items():
#             data = json.loads(data)
#             if data['title1'] not in productList:
#                 productList.append(data['title1'])
#         productList.sort()
#     else:
#         for key, data in redisData.items():
#             data = json.loads(data)
#             if data['title1'] not in productList:
#                 productList.append(data['title1'])
#             if data['title1'] == product:
#                 print(data['title1'])
#                 recomList.append(data)
#         productList.sort()
#     # print("product "+str(product))
#     # print("recomList "+str(recomList))
#     return render_template('recommadation.html', productList=productList, recomList=recomList)




if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)