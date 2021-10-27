from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import Model, SQLAlchemy
from config import Config
from flask_jwt_extended import JWTManager
from waitress import serve
from werkzeug.exceptions import HTTPException

class BaseModel(Model):
    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app, model_class = BaseModel)
migrate = Migrate(app, db)


from server.controllers import product_controller, user_controller