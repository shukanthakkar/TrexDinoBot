"""
Dino Game:

This is a simple implementation of the classic Dino game using the Pygame library.
The game includes a Dino character that can jump over obstacles (cacti) while
earning points. The game ends when the Dino collides with an obstacle.

Classes:
- Background: Represents the scrolling background.
- Dino: Represents the main character of the game.
- Cactus: Represents the obstacles the Dino must avoid.
- Collision: Handles collision detection between objects.
- Score: Manages the scoring system.
- Game: Manages the overall game state.

The game loop in the main function handles updates, rendering, and user input.
"""

import os
import sys
import math
import random
import pygame
import time

# Import the Q-learning classes
from q_learning import DinoStateSpace, QLearningAgent

WIDTH = 623
HEIGHT = 150

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dino')


class Background:
    """
    Class representing the background.

    Attributes:
    - width: Width of the background.
    - height: Height of the background.
    - x: X-coordinate of the background.
    - y: Y-coordinate of the background.
    - texture: Loaded and scaled image representing the background.
    """

    def __init__(self, x):
        """Initialize background object."""
        self.width = WIDTH
        self.height = HEIGHT
        self.x = x
        self.y = 0
        self.set_texture()
        self.show()

    def update(self, dx):
        """Update the background's position."""
        self.x += dx
        if self.x <= -WIDTH:
            self.x = WIDTH

    def show(self):
        """Display the background."""
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(self):
        """Load and scale the background texture."""
        path = os.path.join('assets/images/bg.png')
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))


class Dino:
    """
    Class representing the Dino character.

    Attributes:
    - width: Width of the Dino.
    - height: Height of the Dino.
    - x: X-coordinate of the Dino.
    - y: Y-coordinate of the Dino.
    - texture_num: Current texture index for animation.
    - dy: Vertical speed of the Dino.
    - gravity: Acceleration due to gravity.
    - onground: True if the Dino is on the ground.
    - jumping: True if the Dino is currently jumping.
    - jump_stop: Y-coordinate to stop the jump.
    - falling: True if the Dino is currently falling.
    - fall_stop: Y-coordinate to stop falling.
    - texture: Loaded and scaled image representing the Dino.
    - sound: Loaded sound for the Dino's jump.
    """

    def __init__(self):
        """Initialize Dino object."""
        self.width = 44
        self.height = 44
        self.x = 10
        self.y = 80
        self.texture_num = 0
        self.dy = 3
        self.gravity = 1.0
        self.onground = True
        self.jumping = False
        self.jump_stop = 10
        self.falling = False
        self.fall_stop = self.y
        self.set_texture()
        self.set_sound()
        self.show()

    def update(self, loops):
        """Update Dino's position and state."""
        # jumping
        if self.jumping:
            self.y -= self.dy
            if self.y <= self.jump_stop:
                self.fall()

        # falling
        elif self.falling:
            self.y += self.gravity * self.dy
            if self.y >= self.fall_stop:
                self.stop()

        # walking
        elif self.onground and loops % 4 == 0:
            self.texture_num = (self.texture_num + 1) % 3
            self.set_texture()

    def show(self):
        """Display Dino."""
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(self):
        """Load and scale Dino's texture."""
        path = os.path.join(f'assets/images/dino{self.texture_num}.png')
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

    def set_sound(self):
        """Load Dino's jump sound."""
        path = os.path.join('assets/sounds/jump.wav')
        self.sound = pygame.mixer.Sound(path)

    def jump(self):
        """Handle jumping action."""
        self.sound.play()
        self.jumping = True
        self.onground = False

    def fall(self):
        """Handle falling action."""
        self.jumping = False
        self.falling = True

    def stop(self):
        """Stop falling and set back to onground."""
        self.falling = False
        self.onground = True


class Cactus:
    """
    Class representing the Cactus obstacle.

    Attributes:
    - width: Width of the Cactus.
    - height: Height of the Cactus.
    - x: X-coordinate of the Cactus.
    - y: Y-coordinate of the Cactus.
    - texture: Loaded and scaled image representing the Cactus.
    """

    def __init__(self, x):
        """Initialize Cactus object."""
        self.width = 34
        self.height = 44
        self.x = x
        self.y = 80
        self.set_texture()
        self.show()

    def update(self, dx):
        """Update Cactus's position."""
        self.x += dx

    def show(self):
        """Display Cactus."""
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(self):
        """Load and scale Cactus's texture."""
        path = os.path.join('assets/images/cactus.png')
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))


class Collision:
    """
    Class handling collision detection.

    Methods:
    - between(obj1, obj2): Check if two objects collide.
    """

    def between(self, obj1, obj2):
        """Check if two objects collide."""
        distance = math.sqrt((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2)
        return distance < 35


class Score:
    """
    Class representing the score.

    Attributes:
    - hs: High score.
    - act: Current score.
    - font: Pygame font for rendering text.
    - color: Color of the text.
    - sound: Loaded sound for scoring milestones.
    - lbl: Rendered label for displaying the score.
    """

    def __init__(self, hs):
        """Initialize Score object."""
        self.hs = hs
        self.act = 0
        self.font = pygame.font.SysFont('monospace', 18)
        self.color = (0, 0, 0)
        self.set_sound()
        self.show()

    def update(self, loops):
        """Update the score."""
        self.act = loops // 10
        self.check_hs()
        self.check_sound()

    def show(self):
        """Display the score."""
        self.lbl = self.font.render(f'HI {self.hs} {self.act}', 1, self.color)
        lbl_width = self.lbl.get_rect().width
        screen.blit(self.lbl, (WIDTH - lbl_width - 10, 10))

    def set_sound(self):
        """Load the score sound."""
        path = os.path.join('assets/sounds/point.wav')
        self.sound = pygame.mixer.Sound(path)

    def check_hs(self):
        """Update the high score."""
        if self.act >= self.hs:
            self.hs = self.act

    def check_sound(self):
        """Play a sound for reaching a milestone."""
        if self.act % 100 == 0 and self.act != 0:
            self.sound.play()


class Game:
    """
    Class representing the game state.

    Attributes:
    - bg: List of Background objects for the scrolling background.
    - dino: Dino object representing the main character.
    - obstacles: List of Cactus objects representing obstacles.
    - collision: Collision object for handling collisions.
    - score: Score object for managing the scoring system.
    - speed: Speed of the game.
    - playing: True if the game is currently active.
    - sound: Loaded sound for game over.
    - big_lbl: Rendered label for the game over screen.
    - small_lbl: Rendered label for restarting the game.
    """

    def __init__(self, hs=0):
        """Initialize Game object."""
        self.bg = [Background(x=0), Background(x=WIDTH)]
        self.dino = Dino()
        self.obstacles = []
        self.collision = Collision()
        self.score = Score(hs)
        self.speed = 3
        self.playing = False
        self.set_sound()
        self.set_labels()
        self.spawn_cactus()

    def set_labels(self):
        """Load fonts and labels for game over screen."""
        big_font = pygame.font.SysFont('monospace', 24, bold=True)
        small_font = pygame.font.SysFont('monospace', 18)
        self.big_lbl = big_font.render(f'G A M E  O V E R', 1, (0, 0, 0))
        self.small_lbl = small_font.render(f'press r to restart', 1, (0, 0, 0))

    def set_sound(self):
        """Load game over sound."""
        path = os.path.join('assets/sounds/die.wav')
        self.sound = pygame.mixer.Sound(path)

    def start(self):
        """Start the game."""
        self.playing = True

    def over(self):
        """Game over state."""
        self.sound.play()
        screen.blit(self.big_lbl, (WIDTH // 2 - self.big_lbl.get_width() // 2, HEIGHT // 4))
        screen.blit(self.small_lbl, (WIDTH // 2 - self.small_lbl.get_width() // 2, HEIGHT // 2))
        self.playing = False

    def tospawn(self, loops):
        """Determine if an obstacle should spawn."""
        return loops % 100 == 0

    def spawn_cactus(self):
        """Spawn a new cactus obstacle."""
        # list with cactus
        if len(self.obstacles) > 0:
            prev_cactus = self.obstacles[-1]
            x = random.randint(prev_cactus.x + self.dino.width + 84,
                               WIDTH + prev_cactus.x + self.dino.width + 84)

        # empty list
        else:
            x = random.randint(WIDTH + 100, 1000)

        # create the new cactus
        cactus = Cactus(x)
        self.obstacles.append(cactus)

    def restart(self):
        """Restart the game."""
        self.__init__(hs=self.score.hs)


def main():
    """Main game loop."""

    # objects
    game = Game()
    dino = game.dino
    
    # Q learning
    dino_state_space = DinoStateSpace(dino, game.obstacles)
    actions = ['jump', 'no_jump']

    q_learning_agent = QLearningAgent(dino_state_space, actions)

    # variables
    clock = pygame.time.Clock()
    loops = 0
    over = False

    # main loop
    while True:

        if game.playing:

            loops += 1

            # --- BG ---
            for bg in game.bg:
                bg.update(-game.speed)
                bg.show()

            # --- dino ---
            dino.update(loops)
            dino.show()

            # --- cactus ---
            if game.tospawn(loops):
                game.spawn_cactus()
            

            for cactus in game.obstacles:
                cactus.update(-game.speed)
                cactus.show()
                # Get the current state from the DinoStateSpace
                current_state = dino_state_space.get_state()
    
                # Choose an action using Q-learning agent
                action = q_learning_agent.get_action(current_state)
    
                # Update the Q-value based on the action taken and the resulting state
                # You'll need to define a reward based on the game state
                # For example, you can give a positive reward when Dino successfully jumps over an obstacle
                reward = 0  # Replace with the actual reward mechanism
    
                

                # # collision
                # if game.collision.between(dino, cactus):
                #     over = True
                if game.collision.between(dino, cactus):
                    # Collision occurred, give a negative reward and end the game
                    reward = -50
                    # over = True
                else:
                    # No collision
                    if dino.jumping:
                        # Give a small positive reward for being in the air while jumping
                        reward = 1
                    else:
                        # Give a slightly higher positive reward for staying on the ground
                        reward = 10

                    # If the Dino successfully jumps over an obstacle, give a higher reward
                    if dino.onground and dino.x > cactus.x:
                        reward += 30
                
                # Update Q-value
                q_learning_agent.update_q_value(current_state, action, reward, dino_state_space.get_state())
            if over or game.score.act>999:
                game.over()

            # -- score ---
            game.score.update(loops)
            game.score.show()

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not over:
                        if dino.onground:
                            dino.jump()

                        if not game.playing:
                            game.start()

                if event.key == pygame.K_r:
                    game.restart()
                    dino = game.dino
                    loops = 0
                    over = False

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Automatic actions by Q-learning agent
        if not over and game.playing:
            # Get the current state from the DinoStateSpace
            current_state = dino_state_space.get_state()
        
            # Choose an action using Q-learning agent
            action = q_learning_agent.get_action(current_state)
        
            # Take action based on Q-learning decision
            if action == 'jump' and dino.onground:
                dino.jump()
        
            if action == 'no_jump' and not dino.onground:
                dino.fall()  # Assuming a fall action when not on the ground
                # You might need to adjust this based on your game dynamics
        
            # Start the game if not playing
            if not game.playing:
                game.start()


        clock.tick(80)
        pygame.display.update()


if __name__ == "__main__":
    main()
