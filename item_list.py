import sqlite3
from flask_restful import Resource
from flask_jwt import jwt_required
from db import DB

class ItemList(Resource):

    def get(self):
        
        db = DB()
        connection, cursor = DB.get_connection_read_only()
        cmd = "select * from items"
        result = cursor.execute(cmd)
        rows = result.fetchall()
        DB.close_connection_read_only(connection)
        
        if rows:
            items = []
            for row in rows:
                items.append({"name": row[0], "price": row[1]})
            return {"items": items}

        else:
            return {"message":"No items found"}, 404