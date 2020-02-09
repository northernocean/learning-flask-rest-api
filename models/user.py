import sqlite3
from data_access import DAL
from db import db

class UserModel(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    password = db.Column(db.String(200))

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):

        connection, cursor = DAL.get_connection_read_only()
        cmd = "select * from users where username = ?"
        result = cursor.execute(cmd, (username,))
        row = result.fetchone()
        DAL.close_connection_read_only(connection)
        if row:
            user = cls(*row)
        else:
            user = None
        return user

    @classmethod
    def find_by_id(cls, username):

        connection, cursor = DAL.get_connection_read_only()
        cmd = "select * from users where id = ?"
        result = cursor.execute(cmd, (username,))
        row = result.fetchone()
        DAL.close_connection_read_only(connection)
        if row:
            user = cls(*row)
        else:
            user = None
        return user
