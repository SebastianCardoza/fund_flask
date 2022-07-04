import re
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'keep it secret'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users', methods=['POST'])
def create_users():
    print("Got Post Info")
    session['name'] = request.form['name']
    session['email'] = request.form['email']
    return redirect('/show')

@app.route('/show')
def show_user():
    print('Showing the user info from the form')
    print(session)
    return render_template('show.html')

if __name__ == "__main__":
    app.run(debug=True)