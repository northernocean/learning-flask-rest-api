from flask import Flask
from flask_restful import Api, Resource
from flask_jwt import JWT
from db import db
from datetime import timedelta

from security import authenticate, identity

from resources.user_register import UserRegister
from resources.item import Item
from resources.item_list import ItemList
from resources.store import Store
from resources.store_list import StoreList
from db import db

app = Flask(__name__)
app.secret_key = "david"
app.config["JWT_EXPIRATION_DELTA"] = timedelta(seconds=1800)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
api = Api(app)
jwt = JWT(app, authenticate, identity)

@app.before_first_request
def create_tables():
    pass
    #db.create_all()

# -------------------------------------------------
# A simple example of how this works...
class Student(Resource):
    def get(self, name):
        return {"name": name}
    #def post() ...
    #def delete()...

api.add_resource(Student, "/student/<string:name>")
# -------------------------------------------------

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(UserRegister, "/register")

db.init_app(app)
