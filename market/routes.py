from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, BuyItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/about/<username>')
def about_page(username):
    return f'<h1> This is the about page of {username}</h1>'


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    buy_form = BuyItemForm()
    sell_form = SellItemForm()
    if request.method == 'POST':
        #Buy Item
        bought_item = request.form.get('bought_item')
        b_item_object = Item.query.filter_by(name=bought_item).first()
        if b_item_object:
            if current_user.can_buy(b_item_object):
                b_item_object.buy(current_user)
                flash(f'Thank you for buying {b_item_object.name}!', category='success')
            else:
                flash(f"You can't buy it as it costs more than you have!", category='danger')
        #Sell Item
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f'You just sold {s_item_object.name}!', category='success')
            else:
                flash(f'Something went wrong with selling {b_item_object.name}.', category='danger')
        return redirect(url_for('market_page'))

    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)
        owned_games = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, buy_form=buy_form,
                               owned_games=owned_games, sell_form=sell_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Creating account is finished. You are now logged in {user_to_create.username}', category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for error_message in form.errors.values():
            flash(f'There was an error with creating account: {error_message}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        entered_user = User.query.filter_by(username=form.username.data).first()
        if entered_user and entered_user.check_password_correction(entered_password=form.password.data):
            login_user(entered_user)
            flash(f'Success! You are now logged in {entered_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not correct. Try again or register.', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash(f'Logged out!', category='info')
    return redirect(url_for('home_page'))