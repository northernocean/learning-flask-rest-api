import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from data_access import DAL
from models.item import ItemModel
verbose = False

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
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        else:
            return {"message":"Item not found"}, 404
    
    
    def post(self, name):
        
        if ItemModel.find_by_name(name) is not None:
            return {"error": "Item already exists."}, 400
        else:
            parser = Item.parser
            data = parser.parse_args()
            item = ItemModel(name, data["price"])
            item.insert()

            ItemModel.debug_view_items()

            return item.json(), 200

    
    def put(self, name):
            
        parser = Item.parser
        data = parser.parse_args()

        item = ItemModel.find_by_name(name)
        
        if item is None:
            item.insert()
        else:
            item.price = data["price"]
            item.update()

        return item.json(), 200


    def delete(self, name):
        
        item = ItemModel.find_by_name(name)
        
        if item is not None:    
            item.delete()
            return {"message":"Item deleted"}, 200
        else:
            return {"message":"Item not found"}, 400



        