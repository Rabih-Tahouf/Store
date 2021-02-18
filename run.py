from app import init_app
from db import db

db.init_app(app)

@app.before_first_request  #decorator, run it (method) before first request into this app/ will create data.db file, create tables into this file unless they exist
def create_tables():
    db.create_all()