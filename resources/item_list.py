from flask_restful import Resource
from flask_jwt import jwt_required
from models.item import ItemModel

class ItemList(Resource):

    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}

        