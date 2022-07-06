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
    if request.form['type'] == 'create':
        id = User.save(data)
    elif request.form['type'] == 'update':
        id = request.form['id']
        data['id']=id
        User.update(data)
        
    return redirect(f'/users/{id}')

@app.route('/users/<int:id>')
def show(id):
    user = User.get_user(id)
    return render_template('show.html', user=user)

@app.route('/destroy/<int:id>')
def destroy(id):
    User.delete(id)
    return redirect('/')

@app.route('/update/<int:id>')
def update(id):
    user = User.get_user(id)
    return render_template('update.html', user=user)

if __name__=='__main__':
    app.run(debug=True)
