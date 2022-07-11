from flask_app import app
from flask import render_template, redirect, request
from flask_app.models import ninja, dojo

@app.route('/')
def index():
    return redirect('/dojos')

@app.route('/dojos')
def dojos():
    dojos = dojo.Dojo.get_all()
    return render_template('dojos.html', dojos = dojos)

@app.route('/ninjas')
def ninjas():
    dojos = dojo.Dojo.get_all()
    return render_template('ninjas.html', dojos = dojos)

@app.route('/process', methods=['POST'])
def process():
    if request.form['type'] == 'createdojo':
        print('DOJOOO')
        dojo.Dojo.save({'name': request.form['name']})
        return redirect('/')
    elif request.form['type'] == 'createninja':
        data = {
            'dojo_id':request.form['dojo_id'],
            'first_name':request.form['first_name'],
            'last_name':request.form['last_name'],
            'age':request.form['age']
        }
        ninja.Ninja.save(data)
        return redirect(f'/dojos/{request.form["dojo_id"]}')

@app.route('/dojos/<int:id>')
def get_dojo(id):
    dojo1 = dojo.Dojo.get_dojo_with_ninjas({'id': id})
    return render_template('dojo.html',dojo1 = dojo1)
