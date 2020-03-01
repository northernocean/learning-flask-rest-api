import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, fresh_jwt_required
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
    parser.add_argument("store_id",
        type=float,
        required=True,
        help="store_id is required"
    )

    # --------------
    # public methods
    # --------------
    
    @jwt_required
    def get(self, name):
        #item = next(filter(lambda p: p["name"] == name, items), None)
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        else:
            return {"message":"Item not found"}, 404
    
    @fresh_jwt_required
    def post(self, name):
        
        if ItemModel.find_by_name(name) is not None:
            return {"error": "Item already exists."}, 400
        else:
            data = Item.parser.parse_args()
            item = ItemModel(name, **data)
            item.save_to_db()

            ItemModel.debug_view_items()

            return item.json(), 200

    def put(self, name):
            
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        
        if item is None:
            item = ItemModel(name, **data)
            item.save_to_db()
        else:
            item.price = data["price"]
            item.store_id = data["store_id"]
        
        item.save_to_db()

        return item.json(), 200
    
    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return {"message":"Permission denied."}, 401
        item = ItemModel.find_by_name(name)
        if item is not None:    
            item.delete_from_db()
            return {"message":"Item deleted"}, 200
        else:
            return {"message":"Item not found"}, 400



        