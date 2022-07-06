from flask import Flask, redirect, request, render_template
from user import User

app = Flask(__name__)
app.secret_key = 'keep it secret'

@app.route('/')
def index():
    return redirect('/users')

@app.route('/users')
def users():
    users = User.get_all_users()
    return render_template('index.html', users=users)

@app.route('/users/new')
def create_users():
    return render_template('create.html')

@app.route('/process', methods=['POST'])
def process():
    data = {
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email']
    }
    User.save(data)
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)
