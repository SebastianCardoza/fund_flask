from flask_app import app
from flask_app.models.dojo import Dojo
from flask import redirect, request, session, render_template

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if not Dojo.validate_dojo(request.form):
        return redirect('/')
    data = {
    'nombre':request.form['nombre'],
    'ubicacion':request.form['ubicacion'],
    'idioma':request.form['idioma'],
    'comentario':request.form['comentario']
    }
    id = Dojo.save(data)
    return redirect(f'/result/{id}')

@app.route('/result/<int:id>')
def result(id):
    dojo = Dojo.get_dojo_by_id(id)
    return render_template('result.html', dojo = dojo)