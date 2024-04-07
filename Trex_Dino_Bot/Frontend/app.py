from flask import Flask, render_template

# Import necessary classes and functions from your Dino game
from dino_game import Game

app = Flask(__name__)

# Instantiate the Dino game
#game = Game()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/play')
def play_game():
    # Render the game page
    return render_template('game.html')

if __name__ == "__main__":
    app.run(debug=True,use_reloader=False)
