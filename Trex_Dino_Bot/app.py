from flask import Flask, render_template

# Import DinoGame class from your dino.py file
from Game.dino import DinoGame

app = Flask(__name__, template_folder='Frontend/templates', static_folder='Frontend/static')

# Instantiate the DinoGame class
dino_game = DinoGame(WIDTH=800, HEIGHT=350)  # Adjust WIDTH and HEIGHT as needed

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/play')
def play_game():
    # Render the game page
    return render_template('game.html')

# Add more routes as needed for game actions

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
