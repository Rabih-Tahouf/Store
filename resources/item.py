from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    #TABLE_NAME = 'items'

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)  #now returns an item object as opposed to dict
        if item:
            return item.json()   #therefore we have to conmvert this obj to json, returns item itself
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id']) #this can be inserted into the DB; this is an itemmodel obj, can be **data also

        try:
            item.save_to_db() #calls item itself instead of class
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    @jwt_required()
    def delete(self, name):  #use model to do deletion
       item = ItemModel.find_by_name(name)
       if item:
            item.delete_from_db()
       return {'message':'Item deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        
        if item is None:
            item=ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()  #item uniquely identifited by its id
        return item.json()


class ItemList(Resource):
    #TABLE_NAME = 'items'

    def get(self):
        #i want to return {'items': [item json]}
        return {'items': [item.json() for item in ItemModel.query.all()]} #returns all objects in DB
