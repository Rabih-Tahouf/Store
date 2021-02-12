from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #sqlal db will live at root folder of our porject; can be Mysql, postgreSQL or any other sql enginer
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #turning off "flask sqlal tracker" b/c sqlal has its own modification tracker
app.secret_key = 'Rabih'
api = Api(app)
db.init_app(app)  

@app.before_first_request  #decorator, run it (method) before first request into this app/ will create data.db file, create tables into this file unless they exist
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    app.run(port=5000, debug=True)  # important to mention debug=True
