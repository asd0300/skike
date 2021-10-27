from server import db

    
class Mongo91_data(db.Model):
    __tablename__='data91_data2'
    id = db.Column(db.Integer,nullable =False\
        ,primary_key = True)
    user_id = db.Column(db.String(255),nullable =False)
    created_at = db.Column(db.String(255),nullable =False)
    cid = db.Column(db.String(255) ,nullable =False)
    category = db.Column(db.String(255),nullable =False)
    date = db.Column(db.String(255),nullable =False)
    checkout_step = db.Column(db.String(255),nullable =False)

    def __repr__(self):
        return '<Mongo91Data {}>'.format(self.id)

