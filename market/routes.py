from market import app # harus dipanggil lagi karena program berjalan terpisah, di define lagi
from market.models import Item,User #import usernya untuk di setting di validate
from market import db #agar bisa make db.session.add dibawah
from flask import render_template, redirect, url_for, flash ## nah si redirect ini mau dipake dibawah, dan url_for itu akan kebuka ketika dia mencet button dia bawaan flask #karena masih error, di define lagi
from market import bcrypt


#Keperluan untuk routes
from market.models import Item #untuk menuhin syarat Item.query.all()
from market.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required


#ROUTES
@app.route('/') #decorator = 1 step before function to be executed
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
@login_required
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm() #tarik RegisterForm, jangan lupa'()' agar dia menjadi instance bukan variabel
    if form.validate_on_submit(): ##### ini untuk validate nya
        user_to_create = User(
                            username=form.username.data,
                            email_address=form.email_address.data,
                            password=form.password1.data 
                            ) #ini caranya passing isi fields 
        
        db.session.add(user_to_create) #untuk add session ke db kita
        db.session.commit() #biasanya kalo udh register ke website, kita pindah ke halaman lain kan, nah kita arahin ke /market:
        
        #if user is registered successfully, they are autmatically logged in: 
        login_user(user_to_create)
        flash(f'Account Created Successfully!, You are now logged in as {user_to_create}', category='success')
        
        return redirect(url_for('market_page')) #if user is registered successfully, 'redirect' to market_page
    
    if form.errors != {}: #means, if it catches an error / dictionary is not empty
        for err_msg in form.errors.values(): 
            flash (f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form) 

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit(): #theres 2 function from form. built in, that is validate_ on_submit 
        attempted_user = User.query.filter_by(username=form.username.data).first() #variable to  validate username
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
                ): #conditional for checking the attempted password and password stored
            #if conditional true, then 
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        
        else:
            flash('Username and Password are not match! Please try again', category='danger')

    return render_template('login.html', form=form) 

@app.route('/logout')
def logout_page():
    logout_user() #grab current logged in user and log it out
    flash("You have been logged out!", category='info')

    return redirect(url_for("home_page"))
