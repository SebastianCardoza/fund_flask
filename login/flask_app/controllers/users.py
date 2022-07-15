from datetime import date
from flask_app import app
from flask_app.models.user import User
from flask import redirect, render_template, request, flash, session
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods = ['post'])
def process():
    if request.form['type'] == 'register':
        if not User.validate_register(request.form):
            return redirect('/')
        data = {
            'first_name':request.form['first_name'],
            'last_name':request.form['last_name'],
            'email':request.form['email'],
            'has_belt':request.form['has_belt'] if 'has_belt' in request.form else 0,
            'belt_date':request.form['belt_date'],
            'belt_color':request.form['belt_color'] if 'belt_color' in request.form else '',
            'password':bcrypt.generate_password_hash(request.form['password'])
        }
        session['id'] = User.save(data) 
        flash('Email created succesfully!', category = 'register')
        return redirect('/success')

    if request.form['type'] == 'login':
        user = User.email_in_db(request.form['email'])
        if user == 0 or not bcrypt.check_password_hash(user.password, request.form['password']):
            flash('User/Password is not valid', category= 'login')
            return redirect('/')
        session['id'] = user.id
        return redirect('success')

@app.route('/success')
def success():
    if not 'id' in session:
        return redirect('/')
    print(session['id'])
    user = User.get_user_by_id(session['id'])
    return render_template('success.html',user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
        
