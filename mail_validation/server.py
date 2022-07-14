from flask_app import app
from flask_app.models.mail import Mail
from flask import redirect, render_template, request

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods =['POST'])
def process():
    if not Mail.validate_mail(request.form):
        return redirect('/')
    data = {'address': request.form['address']}
    Mail.save(data)
    print('did save')
    return redirect('/success')

@app.route('/success')
def success():
    mails = Mail.get_all()
    return render_template('success.html', mails = mails)

@app.route('/destroy/<int:id>')
def destroy(id):
    Mail.delete(id)
    return redirect('/success')

if __name__ == '__main__':
    app.run(debug = True)