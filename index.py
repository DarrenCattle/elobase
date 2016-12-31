from src.Player import Player
from src.Database import Database

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'hanzomain'

import flask_login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {'foo': {'pw': 'bar'}}

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    pw = request.form.get('pw')
    #if username not in users:
        #return

    user = User()
    user.id = username

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    #user.is_authenticated = request.form['pw'] == users[username]['pw']

    if Database.nameAvailable(username):
        user.is_authenticated = Database.authenticatePlayer(username,pw)
        return user
    else:
        return

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

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

    if request.form['pw'] == users[username]['pw']:
        user = User()
        user.id = username
        flask_login.login_user(user)
        return redirect(url_for('protected'))

    return 'Bad login'

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



@app.route("/")
def hello():
    return render_template('hello.html')

@app.route("/players")
def players():
    return Database.getPlayerTable()

@app.route("/games")
def games():
    return Database.getGameTable()

if __name__ == "__main__":
    app.run(debug = True)