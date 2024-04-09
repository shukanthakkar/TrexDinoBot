import pyautogui
from Game.dino import DinoGame  # Importing the DinoGame class from dino.py

WIDTH = 600
HEIGHT = 200

def main():
    dino_game = DinoGame(WIDTH, HEIGHT)
    dino_game.run()
    x=dino_game.loops
    print(x)
    if dino_game.game.playing:
        dino_game.display_dino()
        dino_game.display_obstacles()
        dino_game.display_score()
        # Add more display methods as needed

if __name__ == "__main__":
    main()
