from os import environ
from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from db import db
from datetime import timedelta
from blacklist import logged_out_users

from resources.user import User, UserRegister, UserLogin, TokenRefresh, UserLogout
from resources.item import Item
from resources.item_list import ItemList
from resources.store import Store
from resources.store_list import StoreList
from db import db

app = Flask(__name__)
app.secret_key = "david"
app.config["JWT_EXPIRATION_DELTA"] = timedelta(seconds=1800)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DATABASE_URL","sqlite:///data.db")
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access","refresh"]
api = Api(app)
jwt = JWTManager(app)

# jwt documenation:
# https://tools.ietf.org/html/rfc7519
# https://flask-jwt-extended.readthedocs.io/en/latest/index.html

# -----------------
#region jwt_loaders
# -----------------

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True}
    else:
        return {"is_admin": False}

@jwt.token_in_blacklist_loader
def is_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in logged_out_users

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        "description":"The token has expired.",
        "error":"expired token"
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback():
    return jsonify({
        "description":"Signature verification failed.",
        "error":"invalid token"
    }), 401

@jwt.unauthorized_loader
def unauthorized_token_callback():
    return jsonify({
        "description":"Unable to verify token.",
        "error":"missing token"
    }), 401

@jwt.needs_fresh_token_loader
def needs_fresh_token_callback():
    return jsonify({
        "description":"A fresh token is required.",
        "error":"unfresh token"
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description":"Token was revoked.",
        "error":"revoked token"
    }), 401

@app.before_first_request
def create_tables():
    db.create_all()

#endregion

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/refresh")

db.init_app(app)
