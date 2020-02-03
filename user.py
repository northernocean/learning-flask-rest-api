import sqlite3
from flask_restful import Resource, reqparse
from db import DB

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):

        connection, cursor = DB.get_connection_read_only()
        cmd = "select * from users where username = ?"
        result = cursor.execute(cmd, (username,))
        row = result.fetchone()
        DB.close_connection_read_only(connection)
        if row:
            user = cls(*row)
        else:
            user = None
        return user

    @classmethod
    def find_by_id(cls, username):

        connection, cursor = DB.get_connection_read_only()
        cmd = "select * from users where id = ?"
        result = cursor.execute(cmd, (username,))
        row = result.fetchone()
        DB.close_connection_read_only(connection)
        if row:
            user = cls(*row)
        else:
            user = None
        return user

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
        
        if User.find_by_username(data["username"]):
            return {"error":"username already exists."}, 400
        else:
            connection, cursor = DB.get_connection()
            query = "insert into users values (null, ?, ?)"
            cursor.execute(query, (data["username"], data["password"]))
            DB.close_connection(connection, True)
        return {"message":"User created successfully"}, 201


