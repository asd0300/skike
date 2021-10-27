import os,random
from collections import defaultdict
from server import app
from server.models.product_model import create_table,get_products,\
    get_products_variants
from flask import request, render_template
import urllib,json
from server.models.product_model import Product

page_size = 6

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

@app.route('/')
@app.route('/admin/product.html', methods=['GET'])
def admin_product():
    return render_template('product.html')


@app.route('/add', methods=['POST'])
def upload():
    """add proc fun"""
    userDetails = request.form.to_dict() #設userDetails變數
    id = userDetails['id']
    category = userDetails['category']
    title = userDetails['title']
    description = userDetails['description']
    price = userDetails['price']
    texture = userDetails['texture']
    wash = userDetails['wash']
    place = userDetails['place']
    note = userDetails['note']
    story = userDetails['story']
    colors = userDetails['colors']
    sizes = userDetails['sizes']
    # variants = userDetails['variants']
    main_image = request.files['file[]']
    other_files = request.files.getlist('otherfile[]')
    main_image.save(os.path.join(app.root_path,'static','images', 'main',main_image.filename))
    main_image_path = f'static/images/main/{main_image.filename}'
    for other_file in other_files:
        other_file.save(os.path.join(app.root_path,\
            'static','images', 'others', other_file.filename))
    other_files_path = "###".join([f'static/images/others/{str(other_file.filename)}'\
                        for other_file in other_files])
    product2 ={
        'id': id,
        'category': category,
        'title': title,
        'description': description,
        'price': price,
        'texture': texture,
        'wash': wash,
        'place': place,
        'note': note,
        'story': story,
        'colors': colors,
        'sizes': sizes,
        # 'variants': variants,
        'main_image': main_image_path,
        'images': other_files_path,

    }

    # variants = variants.split('/')
    colors = colors.split('/')
    colorCode = []
    variantSize = []
    variantStock =[]
    colorName = []
    # for i in range(0, len(variants), 3):
    #     variantSize.append(variants[i + 1])
    #     variantStock.append(variants[i + 2])
    for j in range(0, len(colors), 2):
        colorName.append(colors[j + 1])
        colorCode.append(colors[j])

    variants2 = [
        {
            "productID":id,
            "color_code": color_code,
            "color_name":color_name,
            "size": size,
            "stock": random.randint(1,10)
        }
        # for (color_code) 
        # in userDetails["colors"].split('/')
        for (color_code,color_name)
        in zip(colorCode,colorName)
        for size in sizes.split('/')
    ]
    
    create_table(product2, variants2)
    return "ok"

@app.route('/api/1.0/products/<category>', methods=['GET'])
def all(category):
    """all proc"""
    categoryList= ['men', 'women', 'accessories', 'all']
    if category in categoryList:
        paging = request.args.get('paging')
        if paging == None or paging == '':
            paging = 0
    res = find_product(category, paging)
    
    products = res.get("products")
    product_count = res.get("product_count")

    if (not products):
        return {"error":'Wrong Request'}
    
    if (not len(products)):
        if (category == 'details'):
            return {"data": None}
        else:
            return {"data": []}
    products_with_detail = \
        get_products_with_detail(request.url_root,products)

    result ={}
    if(product_count > (paging+1)*6):
        result ={
            "data": products_with_detail,
            "next_paging": paging + 1
        }
    else:
        result = {"data": products_with_detail}
    
    return result

def find_product(category,paging):
    if category == 'all':
        return get_products(6,paging, {"category": category})

        # sql = "SELECT * FROM stylish.cloth_product LIMIT {},{}".\
        #     format(str(int(paging)*6),6)
    elif category in ['men', 'women', 'accessories']:
        return get_products(6, paging, {"category": category})

        # sql = "SELECT * FROM stylish.cloth_product where category LIKE '男%' LIMIT {},{}".\
        # format(str(int(paging)*6),6)

        # sql = "SELECT * FROM stylish.cloth_product where category LIKE '女%' LIMIT {},{}".\
        # format(str(int(paging)*6),6)

        # sql = "SELECT * FROM stylish.cloth_product where category LIKE '飾%' LIMIT {},{}".\
        # format(str(int(paging)*6),6)
    elif (category == 'recommend'):
        product_id = request.values["id"]
        return get_products(3, paging, {"recommend": product_id})

def get_products_with_detail(url_root,products):
    product_ids = [p["id"] for p in products]
    variants = get_products_variants(product_ids)
    variants_map = defaultdict(list)
    for variant in variants:
        variants_map[variant['productID']].append(variant)
    
    def parse(product, variants_map):
        product_id = product['id']
        # print("product ",product)
        # print("product_id ", product_id)
        image_path = url_root + 'static/images/' + str(product_id) + '/'
        # print("image_path ", image_path)
        product['main_image'] = image_path + product['main_image']
        # print("product['main_image'] ", product['main_image'])
        product['other_files'] = [image_path + img for img in product['images'].split(',')]
        # print("product['other_files'] ", product['other_files'])
        product_variants = variants_map[product_id]
        # print("product_variants ", product_variants)
        if (not product_variants):
            return product

        product["variants"] = [
            {
                "color_code": v["color_code"],
                "size": v["size"],
                "stock": v["stock"]
            }
            for v in product_variants
        ]
        print('product["variants"] ',product["variants"])
        print('product["colors"] ' ,product["colors"])
        colors = [
            {
                "code": v["color_code"],
                "name": v["color_code"]
            }
            for v in product_variants
        ]
        print('colors ',colors)
        product["colors"] = list({c['code'] + c["name"]: c for c in colors}.values())
        product["sizes"] = list(set([
            v["size"]
            for v in product_variants   
        ]))

        return product
    
    return [
        parse(product, variants_map) for product in products
    ]
