from flask import render_template, redirect, url_for, flash, get_flashed_messages
from flask_login import login_user, logout_user, login_required
from market import app, db, login_manager
from market.models import Item, User
from market.forms import RegisterForm, LoginForm


@app.route('/')
@app.route('/home')
def home_page():  # The name of the function serves as the 'name' of the URL in the Jinja template
    return render_template('home.html')

@app.route('/market')
@login_required
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        user_to_create = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password1.data
        )
        db.session.add(user_to_create)
        db.session.commit()

        attempted_user = User.query.filter_by(username=form.username.data).first()
        login_user(attempted_user)
        flash(f'Logged in successfully. You logged in as {attempted_user.username}', category='success')
        
        return redirect(url_for('market_page'))

    else:
        print(form.errors)
        print(f'User Creation Error(s):')
        for err_msg in form.errors:
            flash(err_msg)
        for err_msg in form.errors.values():
            flash(f"{err_msg}")
    
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.does_password_match(attemped_password=form.password.data):
            login_user(attempted_user)
            flash(f'Logged in successfully. You logged in as {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        
        flash('Username and Password do not match.', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been successfully logged out", category='info')
    return redirect(url_for('home_page'))