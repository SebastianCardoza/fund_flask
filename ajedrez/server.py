from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/<int:rows>')
def rows(rows):
    return render_template('rows.html',num=rows)

@app.route('/<int:rows>/<int:columns>') 
def columns(rows, columns):
    return render_template('columns.html',num=rows, num1=columns)

@app.route('/<int:rows>/<int:columns>/<string:color1>/<string:color2>')
def colors(rows, columns, color1, color2):
    return render_template('colors.html',num=rows, num1=columns, color1=color1, color2=color2)

if __name__ == "__main__":
    app.run(debug=True)