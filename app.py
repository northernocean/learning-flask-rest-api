from flask import Flask
from flask_restful import Api, Resource
from flask_jwt import JWT
from datetime import timedelta

from security import authenticate, identity

from user import UserRegister
from item import Item
from item_list import ItemList

app = Flask(__name__)
app.secret_key = "david"
api = Api(app)

app.config["JWT_EXPIRATION_DELTA"] = timedelta(seconds=1800)
jwt = JWT(app, authenticate, identity)

# -------------------------------------------------
# A simple example of how this works...
class Student(Resource):
    def get(self, name):
        return {"name": name}
    #def post() ...
    #def delete()...

api.add_resource(Student, "/student/<string:name>")
# -------------------------------------------------

api.add_resource(ItemList, "/items")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    app.run()
