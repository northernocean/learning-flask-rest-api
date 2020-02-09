import sqlite3
from data_access import DAL
from db import db

verbose = True

class ItemModel(db.Model):

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200))
    price = db.Column(db.Float(precision=2))

    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    verbose = True
    
    def json(self):
        return {"name": self.name, "price": self.price}

    
    @classmethod
    def find_by_name(cls, name):
        connection, cursor = DAL.get_connection_read_only()
        cmd = "select * from items where name = ?"
        result = cursor.execute(cmd, (name,))
        row = result.fetchone()
        DAL.close_connection_read_only(connection)

        if row:
            return cls(*row)
        else:
            return None
    

    def insert(self):
        
        connection, cursor = DAL.get_connection()
        cmd = "insert into items values (?, ?)"
        cursor.execute(cmd, (self.name,self.price))
        DAL.close_connection(connection, True)
        
        ItemModel.debug_view_items()


    def update(self):
        
        connection, cursor = DAL.get_connection()
        cmd = "update items set price = ? where name = ?"
        cursor.execute(cmd, (self.price, self.name))
        DAL.close_connection(connection, True)
        
        ItemModel.debug_view_items()

    
    def delete(self):
        
        connection, cursor = DAL.get_connection()
        cmd = "delete from items where name = ?"
        cursor.execute(cmd, (self.name,))
        DAL.close_connection(connection, True)
        
        ItemModel.debug_view_items()


    @classmethod
    def debug_view_items(cls):
        
        if(cls.verbose):
            connection, cursor = DAL.get_connection_read_only()
            cmd = "select * from items"
            result = cursor.execute(cmd)
            rows = result.fetchall()
            DAL.close_connection_read_only(connection)

            for row in rows:
                print(row)
        