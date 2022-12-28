#initialization
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app=Flask(__name__)#built in variable, refering to local python file you are working with
#app.config is dictionary that can accept some new values
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///market.db'#kita akan point app kita ke sqlite(tempat db kita) untuk baca isinya
app.config['DEBUG'] = True #for auto debug / auto update
app.config['SECRET_KEY']='fab80fadb03a18668a1c2f9f'

db=SQLAlchemy(app) #for the db

bcrypt=Bcrypt(app)

login_manager=LoginManager(app)
login_manager.login_view = "login_page" #redirect to login page if user not logged in
login_manager.login_message_category = "info"

from market import routes #to run routes.py