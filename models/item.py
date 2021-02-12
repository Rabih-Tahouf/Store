from db import db

class ItemModel(db.Model):
    __tablename__ = 'items' # tables where models will be stored

    id = db.Column(db.Integer, primary_key=True)  # how it will read these items 
    name = db.Column(db.String(80)) #80 characters max. 
    price = db.Column(db.Float(precision=2)) #2dp
    
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')  #sqlAl releives from making joins, it does it for you

    def __init__(self, name, price, store_id):  #these args will come form above 
        self.name = name
        self.price = price 
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}
    
    @classmethod  #becuase it gonna return an object of type item model as oppose to a dict. 
    def find_by_name(cls, name):   #cls: reference to the class
        return cls.query.filter_by(name=name).first() #select * from items where name=name;1st row only; returns item model obj.(name, price)
        # can use either cls or ItemModel, because its a class method

    def save_to_db(self):  #object is self/ can update and insert; upserting, no need anymore for uodate method
        db.session.add(self)   #insert object to DB, session=coll. of objects to write into Db, can add mult obj to sesion and write them all at once
        db.session.commit()     # we are inserting one obj only we are doing adding and commiting str8 after

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        

        