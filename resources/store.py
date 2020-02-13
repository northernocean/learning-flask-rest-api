from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        else:
            return {"message":"store not found"}, 404
    
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"error": "store already exists."}, 400
        else:
            store = StoreModel(name)
            store.save_to_db()
            return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:    
            store.delete_from_db()
            return {"message":"store deleted"}, 200
        else:
            return {"message":"store not found"}, 400



        