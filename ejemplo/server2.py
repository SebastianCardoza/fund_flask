from flask import Flask, render_template,request,redirect
# importar la clase de friend.py
from friend import Friend
app = Flask(__name__)
@app.route("/")
def index():
    # llamar al método de clase get all para obtener todos los amigos
    friends = Friend.get_all()
    return render_template("index.html", friends = friends)

@app.route('/save', methods=['POST'])
def save():
    Friend.save({'fn':request.form['first_name'], 'ln':request.form['last_name'], 'occ':request.form['occupation']})
    return redirect('/')
            
if __name__ == "__main__":
    app.run(debug=True)

