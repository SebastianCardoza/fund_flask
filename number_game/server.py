from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = 'keep it secret'

@app.route('/')
def index():
    if 'number' not in session:
        session['number'] = random.randint(1,100) 
    # If theres a guess number transform it to a int, otherwise put 0
    if 'guess' in session:
        guess = int(session['guess'])
    else:
        guess = 0
    # If theres a number of tries transform it to a int, otherwise put 0
    if 'tries' in session:
        tries = int(session['tries'])
    else:
        tries = 0
    # If the player tries to guess 5 times and doesnt get the number, he loses
    if tries == 5:
        defeat = True
    else:
        defeat = False

    return render_template('index.html', guess=guess, tries=tries, defeat = defeat)

@app.route('/guess', methods=['POST'])
def guess():
    session['guess']=request.form['guess']
    if 'tries' not in session:
        session['tries'] = 1
    else:
        session['tries'] += 1
    return redirect('/')

@app.route('/reset')
def reset():
    session.pop('number')
    session.pop('guess')
    session.pop('tries')
    return redirect('/')

@app.route('/logwinner', methods = ['POST'])
def logwinner():
    if 'winners' not in session:
        session['winners'] = [
            {'name':'Daniel', 'tries': 1},
            {'name':'Jesus', 'tries': 3}
        ]

    session['winners'].append({'name':request.form['name'], 'tries':int(session['tries'])})
    session.modified = True
    print(session['winners'])
    return redirect('/winners')

@app.route('/winners')
def winners():
    print(session['winners'])
    return render_template('winners.html')

if __name__ == '__main__':
    app.run(debug=True)