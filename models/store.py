from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores' # tables where models will be stored

    id = db.Column(db.Integer, primary_key=True)  # how it will read these items 
    name = db.Column(db.String(80)) #80 characters max. 

    items = db.relationship('ItemModel', lazy = 'dynamic')
    
    def __init__(self, name):  #these args will come form above 
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}
    
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
        