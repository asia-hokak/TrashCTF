from flask import *
from register import register
from gevent import pywsgi
from login import login
from dataprocess import *
from datetime import timedelta

import json
import os
import pickle

app = Flask(__name__, static_folder='static')
app.secret_key = os.urandom(16)
app.permanent_session_lifetime = timedelta(days=7)

challenges_file = open('challenges.json', 'r')
chals = json.load(challenges_file)

@app.route('/')
def index():
    check_data()
    return render_template('top.html', current_path = request.path, session = session)

@app.route('/scoreboard')
def view_scoreboard():
    check_data()
    return render_template('scoreboard.html', current_path = request.path, session = session, ranklist = getranklist())

@app.route('/challenges')
def view_challenges():
    check_data()
    return render_template('challenges.html', current_path = request.path, session = session, chals=chals, chal_id = -1)

@app.route('/challenges/<int:chal_id>')
def view_challenges_id(chal_id:int):
    check_data()
    return render_template('challenges.html', current_path = request.path, session = session, chals=chals, chal_id=chal_id)

@app.route('/login')
def view_login():
    return render_template('login.html', current_path = request.path, session = session)

@app.route('/register')
def view_register():
    return render_template('register.html', current_path = request.path, session = session)



@app.route('/user/<int:user_id>')
def view_user(user_id:int):
    check_data()
    return render_template('user.html', current_path = request.path, 
                           chals= chals, 
                           user = getname(user_id), 
                           rank = getrank(user_id),
                            point = getpoint(user_id), 
                            solved_list = getsolve(user_id))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/register', methods=['POST'])
def do_register():
    data = request.json
    username = data['username']
    email    = data['email']
    password = data['password']
    result = register(username, email, password)
    return jsonify(result=result)


@app.route('/login', methods=['POST'])
def do_login():
    data = request.json
    username = data['username']
    password = data['password']
    session_id = session.get('id')
    if session_id is None:
        result, session['id'] = login(username, password)
    else:
        result = 'you are already logged in'
    if result == 'login successful':
        id = session['id']
        session['username'] = getname(id)
        session['data'] = getdata(id)
        session.update()
    return jsonify(result=result)


@app.route('/challenges/<int:chal_id>', methods=['POST'])
def do_challenges(chal_id:int):
    check_data()
    database = sqlite3.connect("userdb.db")
    chal_data = request.json
    flag = chal_data['flag']
    chal = chals[chal_id]
    if flag == chal['flag']:
        if chal_id not in session['data']['solve']:
            session['data']['point'] += chal['point']
            session['data']['solve'].append(chal_id)
            session['data']['correct'] += 1
            session.update()
            result = "correct"
        else:
            result = "you have already solved this challenge"
    else:
        session['data']['incorrect'] += 1
        result = "incorrect"
    data = pickle.dumps(session['data'])
    database.execute("UPDATE USER SET data = ? WHERE id = ?", (data, session['id']))
    database.commit()
    database.close()
    return jsonify(result = result)





def check_data():
    if session.get('data') is None:
        session['data'] = {}
    if session['data'].get('point') is None:
        session['data']['point'] = 0
    if session['data'].get('correct') is None:
        session['data']['correct'] = 0
    if session['data'].get('incorrect') is None:
        session['data']['incorrect'] = 0
    if session['data'].get('solve') is None:
        session['data']['solve'] = []
    session.update()

def run_server():
    server = pywsgi.WSGIServer(('0.0.0.0', 5555), app)
    print('server started at')
    print('http://127.0.0.1:5555')
    server.serve_forever()

def run_server_debug():
    app.run('0.0.0.0', 4444)

if __name__ == '__main__':
    run_server_debug()
    
