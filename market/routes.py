from market import app 
from market.models import Item, User 
from market import db #to execute db lines
from flask import render_template, redirect, url_for, flash, request 


from market.models import Item 
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask_login import login_user, logout_user, login_required, current_user


#ROUTES
@app.route('/') #decorator = 1 step before function to be executed
@app.route('/home')
def home_page():
    return render_template('home.html')



@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    #Purchasing Logic
    purchase_form=PurchaseItemForm()
    selling_form=SellItemForm()
    if request.method == "POST": #similiar to form.validate_on_submit()
        purchased_item = request.form.get('purchased_item') # purchased_item come from identifier in item_modals.html, the output is ={{item.name}}
        p_item_object = Item.query.filter_by(name=purchased_item).first() #for grabbing object itself to be used below
        if p_item_object: #means if not null
            if current_user.can_purchase(p_item_object): #can_purchase coming from models.py defined fun
                p_item_object.buy(current_user) #assign ownership after confirmation
                #buy() comes from models.py

                flash(f'Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$', category='success')

            else:
                flash(f'Sorry, your budget is not enough to buy {p_item_object.name} for {p_item_object.price}$', category='danger')

        #Selling Logic
        sold_item=request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object: 
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user) #Let go of ownership + give money back 

                flash(f'Congratulations! You sold {s_item_object.name} for {s_item_object.price}$', category='success')

            else:
                flash(f"Sorry, something went wrong with selling {p_item_object.name}", category='danger')

        return redirect(url_for('market_page'))
    

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items= Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, selling_form=selling_form, owned_items=owned_items)



@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm() #'()' is necessary to get it as an instance, not variable 
    if form.validate_on_submit(): #This is to submitting, #theres 2 function from form. It's built in, and that is validate_ & on_submit 
        user_to_create = User(
                            username=form.username.data,
                            email_address=form.email_address.data,
                            password=form.password1.data 
                            ) #this is how to pass fields content
        
        db.session.add(user_to_create) #adding data to db
        db.session.commit() 
        
        #if user is registered successfully, they are autmatically logged in: 
        login_user(user_to_create)
        flash(f'Account created successfully! You are now logged in as {user_to_create}', category='success')
        
        #if user is registered successfully, 'redirect' to market_page:
        return redirect(url_for('market_page')) 
    
    if form.errors != {}: #means, if it catches an error / dictionary is not empty
        for err_msg in form.errors.values(): 
            flash (f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form) 



@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit(): 
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
