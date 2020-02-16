import sqlite3
from data_access import DAL
from db import db

verbose = True

class ItemModel(db.Model):

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel")

    verbose = False
    
    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return ( 
            {
                "name": self.name,
                "price": self.price,
                "store_id": self.store_id
            })

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
   
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

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
