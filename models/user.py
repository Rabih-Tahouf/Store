import sqlite3
from db import db

class UserModel(db.Model):  #this is an api, not a rest one, exposes 2 ednpoints/methods/ 
    #they are interface for other parts of the progrmm to interact with the user thing; 
    #like writing into db and retreiving from it
    #as long as we dont change the api, we dont have to worry about the impact of our changes anywhere else in the code
    __tablename__ = 'users' # tables where models will be stored

    id = db.Column(db.Integer, primary_key=True) #(auto incremented) will automatically be assigned/created, u dont have to create it
    username = db.Column(db.String(80)) #80 characters max. 
    password = db.Column(db.String(80))
    #when u create an obj thru sqlal id will be given to you 
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def save_to_db(self):
        db.session.add(self)   
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):  #also an api/security.py uses this to comm with a user and db
        return cls.query.filter_by(username = username).first() #query: querybuilder: and obj that allows us to buildd queries
        
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id = _id).first() #query: querybuilder: and obj that allows us to buildd queries