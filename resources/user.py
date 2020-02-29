import sqlite3
from flask_restful import Resource, reqparse
from data_access import DAL
from models.user import UserModel


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

    parser = reqparse.RequestParser()
    parser.add_argument("username",
        type=str,
        required=True,
        help="This field cannot be left blank"
    )
    parser.add_argument("password",
       type=str,
       required=True,
       help="This field is required" 
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data["username"]):
            return {"error":"username already exists."}, 400
        else:
            user = UserModel(None, **data)
            user.save_to_db()
            return {"message":"User created successfully"}, 201
