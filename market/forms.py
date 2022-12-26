from flask_wtf import FlaskForm

#special fields untuk form yang akan diisi
from wtforms import StringField, PasswordField, SubmitField

#validators
from wtforms.validators import Length, EqualTo, Email, DataRequired
#EqualTo untuk password
#'Email' Checks if its really an email address


class RegisterForm(FlaskForm): 
    username = StringField(label='User Name:', validators=[Length(min=4, max=30), DataRequired()])
    email_address = StringField(label='Your Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6, max=40), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account') #label = tulisan didalem button