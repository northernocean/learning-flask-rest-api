import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from db import DB

verbose = True

# 200 OK
# 201 Created
# 400 Bad Request
# 401 Unauthorized	
# 403 Forbidden
# 404 Not Found
# 405 Method Not Allowed (The resource doesn't support the specified HTTP verb)
# 409 Conflict
# 411 Length Required (The Content-Length header was not specified)
# 412 Precondition Failed
# 429 Too Many Requests
# 500 Internal Server Error
# 503 Service Unavailable

class Item(Resource):
    
    # ----------------
    # class properties
    # ----------------
    parser = reqparse.RequestParser()
    parser.add_argument("price",
        type=float,
        required=True,
        help="This field cannot be left blank"
    )

    # --------------
    # public methods
    # --------------
    @jwt_required()
    def get(self, name):
        #item = next(filter(lambda p: p["name"] == name, items), None)
        item = Item.find_by_name(name)
        if item:
            return item, 200
        else:
            return {"message":"Item not found"}, 404
    
    
    def post(self, name):
        
        if Item.find_by_name(name)[1] == 200:
            return {"error": "Item already exists."}, 400
        else:
            parser = Item.parser
            data = parser.parse_args()
            
            item = {"name": name, "price":data["price"]}
            Item.insert_item(item)

            Item.debug_view_items()

            return item, 200

    
    def put(self, name):
            
        parser = Item.parser
        data = parser.parse_args()

        item = {"name": name, "price": data["price"]}
        
        if Item.find_by_name(name)[1] == 200:
            Item.update_item(item)
        else:
            Item.insert_item(item)

        return item, 200


    def delete(self, name):
        
        if Item.find_by_name(name)[1] == 200:
            query = "delete from items where name = ?"
            connection, cursor = DB.get_connection()
            result = cursor.execute(query, (name,))
            DB.close_connection(connection, True)

            Item.debug_view_items()

            return {"message":"Item deleted"}, 200

        else:
            return {"message":"Item not found"}, 400

    # ---------------
    # private methods
    # ---------------
    @classmethod
    def find_by_name(cls, name):
        
        connection, cursor = DB.get_connection_read_only()
        cmd = "select * from items where name = ?"
        result = cursor.execute(cmd, (name,))
        row = result.fetchone()
        DB.close_connection_read_only(connection)

        if row:
            return {"item": {"name": row[0], "price":row[1]}}, 200
        else:
            return {"message":"Item not found"}, 404
    

    @classmethod
    def insert_item(cls, item):
        
        connection, cursor = DB.get_connection()
        cmd = "insert into items values (?, ?)"
        cursor.execute(cmd, (item["name"],item["price"]))
        DB.close_connection(connection, True)
        
        Item.debug_view_items()


    @classmethod
    def update_item(cls, item):
        
        connection, cursor = DB.get_connection()
        cmd = "update items set price = ? where name = ?"
        cursor.execute(cmd, (item["price"], item["name"]))
        DB.close_connection(connection, True)
        
        Item.debug_view_items()


    @classmethod
    def debug_view_items(cls):
        
        global verbose
        
        if(verbose):
            connection, cursor = DB.get_connection_read_only()
            cmd = "select * from items"
            result = cursor.execute(cmd)
            rows = result.fetchall()
            DB.close_connection_read_only(connection)

            for row in rows:
                print(row)


        