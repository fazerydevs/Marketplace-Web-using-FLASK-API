from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Models for User
class User(db.Model, UserMixin):
    id= db.Column(db.Integer(), primary_key=True)
    username       = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address  = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash  = db.Column(db.String(60), nullable=False) 
    budget         = db.Column(db.Integer(), nullable=False, default=10000) 
    items          = db.relationship('Item', backref='owned_user', lazy=True)

    def __repr__(self):
        return f'Item {self.username}'

    #properties to make budget '10,000' not '100000'
    @property
    def prettier_budget(self):
        if len(str(self.budget))>=4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$' #if it's overwhelming, breakdown 1 by 1
        else:
            return f"{self.budget}$"

    #Getter of Password hashing 
    @property
    def password(self): 
        return self.password #I have new property, and I basically return the password back when user wants it
    
    #Setter, Hashing password in db 
    @password.setter 
    def password(self, plain_text_password): 
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8') #overwrite password fields with password_hash


    #Function for veryfing password when a User try to login, used in routes.py
    def check_password_correction(self, attempted_password): 
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    #Function for veryfing the user Budget is sufficient to buy items, used in routes.py
    def can_purchase(self, item_obj): 
        return self.budget >= item_obj.price #return boolean (True/False)

    #Function for veryfing is the user have the item to sell 
    def can_sell(self, item_obj):
        return item_obj in self.items #checking with backref in Class User, items


#Models for Item
class Item(db.Model):
    id          = db.Column(db.Integer(), primary_key=True) #id in models is compulsory, because flask is automatically differentiate every object with ID 
    price       = db.Column(db.Integer(), nullable=False)
    barcode     = db.Column(db.String(length=20), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False)
    owner       = db.Column(db.Integer(), db.ForeignKey('user.id')) # Owner of an item is unique only 1 user can have it so we set db.foreignkey as user.id 

    #Function if someone buy an item from market, used in routes.py
    def buy(self,user):
        self.owner = user.id 
        user.budget -= self.price
        db.session.commit()
    
    #Function if someone sell an item from market, used in routes.py
    def sell(self,user):
        self.owner = None
        user.budget += self.price 
        db.session.commit() 

    def __repr__(self):
        return f'Item {self.name}' 