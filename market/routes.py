from market import app # harus dipanggil lagi karena program berjalan terpisah, di define lagi
from market.models import Item,User #import usernya untuk di setting di validate
from market import db #agar bisa make db.session.add dibawah
from flask import render_template, redirect, url_for ## nah si redirect ini mau dipake dibawah, dan url_for itu akan kebuka ketika dia mencet button dia bawaan flask #karena masih error, di define lagi

#Keperluan untuk routes
from market.models import Item #untuk menuhin syarat Item.query.all()
from market.forms import RegisterForm


#ROUTES
@app.route('/') #decorator = 1 step before function to be executed
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
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
                            password_hash=form.password1.data
                            ) #ini caranya passing isi fields 
        
        db.session.add(user_to_create) #untuk add session ke db kita
        db.session.commit() #biasanya kalo udh register ke website, kita pindah ke halaman lain kan, nah kita arahin ke /market:
        return redirect(url_for('market_page')) #url_for untuk ketika dipencet, kita arah kemana ? kita 'redirect' ke market_page
    
    return render_template('register.html', form=form) 