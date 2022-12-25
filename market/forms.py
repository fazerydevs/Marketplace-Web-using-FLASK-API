from flask_wtf import FlaskForm

#special fields untuk form yang akan diisi
from wtforms import StringField, PasswordField, SubmitField


class RegisterForm(FlaskForm): 
    username = StringField(label='User Name:')
    email_address = StringField(label='Your Email Address:')
    password1 = PasswordField(label='Password:')
    password2 = PasswordField(label='Confirm Password:')
    submit = SubmitField(label='Create Account') #label = tulisan didalem button