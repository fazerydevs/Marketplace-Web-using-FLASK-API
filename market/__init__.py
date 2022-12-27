#initialization
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app=Flask(__name__)#built in variable, refering to local python file you are working with
#app.config adalah dictionary yang akan accept some new values
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///market.db'#kita akan point app kita ke sqlite(tempat db kita) untuk baca isinya
app.config['DEBUG'] = True #untuk auto debug / auto update
app.config['SECRET_KEY']='fab80fadb03a18668a1c2f9f'

db=SQLAlchemy(app) #for the db

bcrypt=Bcrypt(app)

from market import routes #untuk jalanin routes.py