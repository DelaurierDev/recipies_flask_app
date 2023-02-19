from flask_app import app
from flask import render_template, redirect,request,session,flash
import re
from flask_app.models.user import User
from flask_app.models.recipie import Recipie
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def login_reg():
    return render_template('index.html')

@app.route('/dashboard')
def logged_in():
    if 'user_id' not in session:
        flash('Must login')
        return redirect('/')
    
    return render_template('dashboard.html',
                            user_name = session['first_name'],
                            user_id = session['user_id'],
                            recipies = Recipie.getAllRecipies())

@app.route('/register', methods=['POST'])
def create_user():

    data = {'email': request.form['email']}
    user_in_db = User.get_by_email(data)
    if not User.validate_user(request.form):
        return redirect('/')

    

    if user_in_db:
        flash('Email already exists. Please Log In')
        return redirect('/')
    passhash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        'fname' : request.form['fname'],
        'lname' : request.form['lname'],
        'email' : request.form['email'],
        'password' : passhash
    }
    user_id = User.save_user(data)
    session['user_id'] = user_id
    session['first_name'] = data['fname']
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data = {'email': request.form['email']}
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash('Invalid Email/Password')
        return redirect('/')
    
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password')
        return redirect('/')
    
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name

    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
