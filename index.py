from src.Player import Player
from src.Database import Database
from flask import Flask, render_template
app = Flask(__name__)

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