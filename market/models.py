from market import db
from market import bcrypt

class User(db.Model):
    id= db.Column(db.Integer(), primary_key=True)
    username       = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address  = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash  = db.Column(db.String(length=60), nullable=False) #password gabisa pake string, pake hashing algorithm/encryption
                    #flask hash max length = 60, unique gaperlu karena 2 user password sama gpp
    budget         = db.Column(db.Integer(), nullable=False, default=1000) #uang yang dimiliki user
    items          = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def password(self): 
        return self.password #I have new property, and I basically return it back when user wants it
    
    @password.setter 
    def password (self, plain_text_password): #we execute some lines of codes before actually set a password to an user instances
        #overwrite si password_hash di atas 
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8') 
    
#models / kolom dari db
#model item dibawah ajaa
class Item(db.Model):
    id          = db.Column(db.Integer(), primary_key=True) #id di model itu wajib karena flask akan membedakan item dengan id
    name        = db.Column(db.String(length=30), nullable=False, unique=True)
    price       = db.Column(db.Integer(), nullable=False, unique=True)
    barcode     = db.Column(db.String(length=20), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False)
    owner       = db.Column(db.Integer(), db.ForeignKey('user.id')) #user.id in lowercase


    def __repr__(self):
        return f'Item {self.name}' #ini dipake agar pas di cari ga keluar <object 012804810>