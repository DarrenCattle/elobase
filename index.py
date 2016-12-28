from src.Player import Player
from src.Database import Database
from flask import Flask
app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/players")
def players():
    p = Player
    return p.getPlayer(1)

if __name__ == "__main__":
    app.run()