import sqlite3
from blacklist import logged_out_users
from flask_restful import Resource, reqparse
from data_access import DAL
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                    jwt_refresh_token_required,
                                    get_jwt_identity, jwt_required,
                                    get_raw_jwt)

_parser = reqparse.RequestParser()

_parser.add_argument("username",
    type=str,
    required=True,
    help="This field cannot be left blank"
)
_parser.add_argument("password",
    type=str,
    required=True,
    help="This field is required" 
)

class User(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        else:
            return user.json()
    
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        else:
            user.delete_from_db()
            return {"message": "User deleted"}, 200


class UserRegister(Resource):

    def post(self):
        data = _parser.parse_args()
        if UserModel.find_by_username(data["username"]):
            return {"error":"username already exists."}, 400
        else:
            user = UserModel(None, **data)
            user.save_to_db()
            return {"message":"User created successfully"}, 201


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = _parser.parse_args()
        user = UserModel.find_by_username(data["username"])
        if user and safe_str_cmp(user.password, data["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200
        else:
            return {
                "message": "invalid credentials"
            }, 401


class UserLogout(Resource):
    
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"] # jti = jwt (unique) identifier
        logged_out_users.add(jti)
        return {"message": "Successfully logged out."}, 200


class TokenRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        user = get_jwt_identity()
        new_token = create_access_token(identity=user, fresh=False)
        return {"access_token": new_token}, 200
