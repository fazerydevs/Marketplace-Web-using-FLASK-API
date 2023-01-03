from flask_wtf import FlaskForm

#special fields untuk form yang akan diisi
from wtforms import StringField, PasswordField, SubmitField

#validators
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
#EqualTo untuk password
#'Email' Checks if its really an email address
from market.models import User

class RegisterForm(FlaskForm): 

    #same username validation
    def validate_username(self, username_to_check):
        user=User.query.filter_by(username=username_to_check.data).first() #.data untuk passing fields seperti di routes.py
        if user: #if thereis user
            raise ValidationError('Username Already Exists! Please Try Another Username')

    #same email validation
    def validate_email_address(self, email_address_to_check):
        email_address=User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address: #if thereis 
            raise ValidationError('Email Address Already Exists! Please Try Another Email Address')

    username = StringField(label='User Name:', validators=[Length(min=4, max=30), DataRequired()])
    email_address = StringField(label='Your Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6, max=40), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account') #label = tulisan didalem button

class LoginForm(FlaskForm): 
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item')
        
class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item')
