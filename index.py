from src.player import Player
from src.database import Database
from src.actions import Actions

from flask import Flask, render_template, render_template_string, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'hanzomain'

import flask_login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    #if username not in users:
        #return

    user = User()
    user.id = username
    return user

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    pw = request.form.get('pw')
    #if username not in users:
        #print(username)
        #return

    user = User()
    user.id = username

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    #user.is_authenticated = request.form['pw'] == users[username]['pw']

    #print(username, Database.nameAvailable(username))
    #return user

    if username is not None and Actions.name_available(username):
        user.is_authenticated = Actions.authenticate_user(username, pw)
        return user
    return

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

@app.route('/')
def default():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
           <form action='login' method='POST'>
            <input type='text' name='username' id='username' placeholder='username'></input>
            <input type='password' name='pw' id='pw' placeholder='password'></input>
            <input type='submit' name='submit'></input>
           </form>
           '''

    username = request.form['username']
    pw = request.form['pw']
    print(username, pw)

    if Actions.authenticate_user(username,pw):
        user = User()
        user.id = username
        flask_login.login_user(user)
        return redirect(url_for('dashboard'))

    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out' + '''<br>
        <a href="/login">Login</a>'''

@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id + '''<br>
            <a href="/logout">Logout</a>
        '''

@app.route('/dashboard')
@flask_login.login_required
def dashboard():
    return render_template('dash.html',
                           name=flask_login.current_user.id,
                           games=Actions.get_games(),
                           players=Actions.get_users())

@app.route('/creategame', methods=['GET', 'POST'])
@flask_login.login_required
def creategame():
    if request.method == 'GET':
        return '''
           <form action='creategame' method='POST'>
            <input type='text' name='game' id='game' placeholder='game'></input>
            <input type='submit' name='submit'></input>
           </form>
           '''

    game = request.form['game']
    if game is not None:
        Actions.create_game_tables(game)

    return redirect(url_for('dashboard'))

@app.route('/deletegame', methods=['GET', 'POST'])
@flask_login.login_required
def deletegame():
    if request.method == 'GET':
        return '''
           <form action='deletegame' method='POST'>
            <input type='text' name='game' id='game' placeholder='game'></input>
            <input type='submit' name='submit'></input>
           </form>
           '''

    game = request.form['game']
    if game is not None:
        Actions.delete_game_tables(game)

    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run(debug = True)