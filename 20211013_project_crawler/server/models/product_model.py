from server import db
# from server.models.recommendation_model import SimilarityModel
    
class Product(db.Model):
    __tablename__='products2'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer ,nullable =False\
        ,primary_key = True)
    category = db.Column(db.String(255),nullable =False)
    title = db.Column(db.TEXT,nullable =False)
    description = db.Column(db.TEXT,nullable =False)
    price = db.Column(db.Integer ,nullable =False)
    texture = db.Column(db.TEXT,nullable =False)
    wash = db.Column(db.TEXT,nullable =False)
    place = db.Column(db.String(255),nullable =False)
    note = db.Column(db.TEXT,nullable =False)
    story = db.Column(db.TEXT,nullable =False)
    colors = db.Column(db.TEXT,nullable =False)
    sizes = db.Column(db.TEXT,nullable =False)
    # variants = db.Column(db.TEXT,nullable =False)
    main_image = db.Column(db.TEXT,nullable =False)
    images = db.Column(db.TEXT,nullable =False)

    def __repr__(self):
        return '<Product {}, {}, {}>'.format(self.id, self.title, self.price)

class Colors(db.Model):
    __tablename__='Color2'
    itemID = db.Column(db.Integer,nullable =False\
        , primary_key=True)
    productID = db.Column(db.Integer,db.ForeignKey('products2.id'),nullable =False, )
    name = db.Column(db.String(20),nullable =False)
    code = db.Column(db.String(20) ,nullable =False)

    def __repr__(self):
        return '<Colors {}>'.format(self.productID)

class Variant(db.Model):
    __tablename__='variant2'
    itemID = db.Column(db.Integer,nullable =False\
        , primary_key=True)
    productID = db.Column(db.Integer,db.ForeignKey('products2.id'),nullable =False)
    color_name = db.Column(db.String(20),nullable =False)
    color_code = db.Column(db.String(20) ,nullable =False)
    size = db.Column(db.String(20) ,nullable =False)
    stock = db.Column(db.String(20) ,nullable =False)

    def __repr__(self):
        return '<Variant {}>'.format(self.productID)

class Image_Main(db.Model):
    __tablename__='main_image2'
    urlID = db.Column(db.Integer,nullable =False\
        , primary_key=True)
    productID = db.Column(db.Integer,db.ForeignKey('products2.id'),nullable =False, )
    url = db.Column(db.TEXT,nullable =False)

    def __repr__(self):
        return '<Image_Main {}>'.format(self.productID)

class Image_Others(db.Model):
    __tablename__='other_images2'
    urlID = db.Column(db.Integer,nullable =False\
        , primary_key=True)
    productID = db.Column(db.Integer,db.ForeignKey('products2.id'),nullable =False, )
    url = db.Column(db.TEXT,nullable =False)

    def __repr__(self):
        return '<Image_Others {}>'.format(self.productID)


def create_table(product, variants):
    product_model = Product(**product)
    db.session.add(product_model)
    db.session.flush()

    db.session.bulk_insert_mappings(
        Variant,
        variants
    )
    db.session.commit()

db.create_all()

def get_products(page_size, paging, requirement ={}):
    if("category" in requirement):
        category = requirement.get('category')
        if (category == "all"):
            product_query = Product.query
        elif(category == "men"):
            product_query = Product.query.filter_by(category = "men")
        elif(category == "women"):
            product_query = Product.query.filter_by(category = "women")
        elif(category == "accessories"):
            product_query = Product.query.filter_by(category = "accessories")
    elif ("recommend" in requirement):
        product_query = Product.query.join(SimilarityModel, Product.id == SimilarityModel.item2_id)\
            .filter_by(item1_id = requirement.get("recommend"))\
            .order_by(SimilarityModel.similarity.desc()).get_product


    products = product_query.limit(page_size).offset(page_size * paging).all()
    
    count = product_query.count()
    return{
        "products": [p.to_json() for p in products],
        "product_count": count
    }

def get_products_variants(product_ids):
    variants = Variant.query.filter(Product.id.in_(product_ids)).all()
    return[v.to_json() for v in variants]