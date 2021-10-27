from server import db

class User(db.Model):
    __tablename__='user2'
    id = db.Column(db.Integer,nullable =False\
        , primary_key=True)
    provider = db.Column(db.String(20),nullable =False)
    name = db.Column(db.String(20),nullable =False)
    email = db.Column(db.String(255) ,nullable =False)
    password = db.Column(db.String(255) ,nullable =False)
    picture = db.Column(db.TEXT ,nullable =False)
    access_token = db.Column(db.String(255) ,nullable =False)
    access_expired = db.Column(db.String(255) ,nullable =False)
    facebookID = db.Column(db.String(255) ,nullable =False)

    def __repr__(self):
        return '<Product {}>'.format(self.id)