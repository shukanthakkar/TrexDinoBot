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
from PIL import  Image
import pandas as pd


WIDTH = 600
HEIGHT = 200

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((255,255,255))
pygame.display.set_caption('Dino')


assets={}
# Read the CSV file using pandas
df = pd.read_csv('assets\\images\\resources.csv')

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    # Extract information from the row
    resourceName = row['resourceName']
    x1, y1, x2, y2 = int(row['X1']), int(row['Y1']), int(row['X2']), int(row['Y2'])
    
    # Open the image file
    image = Image.open('assets\\images\\resources.png')
    
    # Crop the image based on the provided coordinates
    cropped_image = image.crop((x1, y1, x2, y2))
    
    # Convert the cropped image to RGB mode to remove any alpha channel
    cropped_image = cropped_image.convert("RGB")
    
    # Create a new white background image with the same dimensions as the cropped image
    # background = Image.new('RGB', cropped_image.size, color='white')
    
    # Paste the cropped image onto the white background
    # background.paste(cropped_image, (0, 0))
    
    background=cropped_image
    
    background=background.convert('RGBA')
    
    background=background.resize(list(map(lambda x:x//2 , background.size)))
    
    assets[resourceName]=background


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
        self.y = 150
        self.set_texture()
        self.show()

    def update(self, dx):
        """Update the background's position."""
        self.x += dx
        if self.x <= -WIDTH:
            self.x = WIDTH

    def show(self):
        """Display the background."""
        # screen.blit(self.texture, (self.x, self.y))
        
        # bg = (0, 150)
        # bg1 = (600,150)
        screen.blit(pygame.image.fromstring(self.texture.tobytes(), self.texture.size, 'RGBA'), (self.x,self.y))
        # screen.blit(pygame.image.fromstring(self.texture.tobytes(), self.texture.size, 'RGBA'), bg1)

    def set_texture(self):
        """Load and scale the background texture."""
        
        # path = os.path.join('assets/images/bg.png')
        path = os.path.join('assets/images/ground.png')
        # self.texture = pygame.image.load(path)
        
        self.texture=assets['ground']#Image.open(path).convert("RGBA")
        
        # self.texture=self.texture.resize(list(map(lambda x:x//2 , self.texture.size)))
        # self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

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
        self.x = 5#10
        self.y = 110
        self.texture_num = 0
        self.dy = 3
        self.gravity = 1.2
        self.onground = True
        self.collided=False
        self.jumping = False
        self.jump_stop = 10
        self.falling = False
        self.ducking = False
        self.fall_stop = self.y
        self.set_texture()
        #self.set_texture_duck()
        self.set_sound()
        self.set_sound_duck()
        self.show()

    def update(self, loops):
        """Update Dino's position and state."""
        # ducking
        if self.collided:
            self.texture_num = 1#(self.texture_num + 1) % 2
            self.set_texture_collided()
        # jumping
        elif self.jumping:
            self.y -= self.dy
            if self.y <= self.jump_stop:
                self.fall()

        # falling
        elif self.falling:
            self.y += self.gravity * self.dy
            if self.y >= self.fall_stop:
                self.stop()

        # walking
        elif self.onground and loops % 4 == 0 and not self.ducking:
            self.texture_num = (self.texture_num + 1) % 3
            self.set_texture()
        
        # ducking
        elif self.onground and loops % 4 == 0 and self.ducking:
            self.texture_num = (self.texture_num + 1) % 2
            self.set_texture_duck()
                

    def show(self):
        """Display Dino."""
        # screen.blit(self.texture, (self.x, self.y))
        
        screen.blit(pygame.image.fromstring(self.texture.tobytes(), self.texture.size, 'RGBA'), (self.x, self.y))
        
        # if not self.ducking:
        #     screen.blit(self.texture, (self.x, self.y))
        # elif self.ducking:
        #     screen.blit(self.texture, (self.x, self.y+8))
        
    def set_texture(self):
        """Load and scale Dino's texture."""
        path = os.path.join(f'assets/images/dino{self.texture_num}.png')
        
        self.texture = assets[f'dino{self.texture_num}']#pygame.image.load(path)
        
        # self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

    def set_texture_duck(self):
        """Load and scale Dino's texture."""
        path = os.path.join(f'assets/images/dino_duck{self.texture_num}.png')
        
        self.texture = assets[f'dino_duck{self.texture_num}']#pygame.image.load(path)
        
        # self.texture = pygame.transform.scale(self.texture, (self.width, self.height-12))

    def set_texture_collided(self):
        """Load and scale Dino's texture."""
        path = os.path.join(f'assets/images/dino_stuck{self.texture_num}.png')
        
        self.texture = assets[f'dino_stuck{self.texture_num}']#pygame.image.load(path)
        
        # self.texture = pygame.transform.scale(self.texture, (self.width, self.height-12))

    def set_sound(self):
        """Load Dino's jump sound."""
        path = os.path.join('assets/sounds/jump.wav')
        self.sound = pygame.mixer.Sound(path)

    def set_sound_duck(self):
        """Load Dino's duck sound."""
        path = os.path.join('assets/sounds/duck.wav')
        self.soundduck = pygame.mixer.Sound(path)

    def jump(self):
        """Handle jumping action."""
        self.sound.play()
        self.jumping = True
        self.onground = False

    def duck(self):
        """Handle jumping action."""
        self.soundduck.play()
        self.ducking = True

    def duckrelease(self):
        """Handle jumping action."""
        self.ducking = False

    def fall(self):
        """Handle falling action."""
        self.jumping = False
        self.falling = True

    def stop(self):
        """Stop falling and set back to onground."""
        self.falling = False
        self.onground = True
    
    def collide(self):
        self.collided=True


class Bird:
    """
    Class representing the bird obstacle.

    Attributes:
    - width: Width of the Bird.
    - height: Height of the Bird.
    - x: X-coordinate of the Bird.
    - y: Y-coordinate of the Bird.
    - texture: Loaded and scaled image representing the Bird.
    """

    def __init__(self, x):
        """Initialize Birt object."""
        self.type="Bird"
        self.width = 40
        self.height = 30
        self.texture_num = 0 
        self.flying=True
        self.x = x
        self.y = random.randint(20,80)
        self.set_texture()
        self.show()

    def update(self, dx):
        """Update Bird's position."""
        self.x += dx
        #self.y += random.randint(-3, 3)

    def show(self):
        """Display Bird."""
        
        # screen.blit(self.texture, (self.x, self.y))
        
        screen.blit(pygame.image.fromstring(self.texture.tobytes(), self.texture.size, 'RGBA'), (self.x, self.y))
    def set_texture(self):
        """Load and scale Dino's texture."""
        # path = os.path.join(f'assets/images/bird{self.texture_num}.png')
        
        self.texture = assets[f'bird{self.texture_num}']#pygame.image.load(path)
        
        # self.texture = pygame.transform.scale(self.texture, (self.width, self.height))
        
    def update_fly(self,loops):
        """Update Dino's position and state."""
        # ducking
        if self.flying and loops % 10 == 0:
            self.texture_num = (self.texture_num + 1) % 2
            self.set_texture()
        
class Cloud:
    """
    Class representing the Cactus obstacle.

    Attributes:
    - width: Width of the Cactus.
    - height: Height of the Cactus.
    - x: X-coordinate of the Cactus.
    - y: Y-coordinate of the Cactus.
    - texture: Loaded and scaled image representing the Cactus.
    """

    def __init__(self,x):
        """Initialize Cactus object."""
        self.type="Cactus"
        self.width = 34
        self.height = 44
        self.x = x
        self.y = random.randint(10, 100)
        self.set_texture()
        self.show()

    def update(self, dx):
        """Update Cactus's position."""
        self.x += dx

    def show(self):
        """Display Cactus."""
        # screen.blit(self.texture, (self.x, self.y))
        screen.blit(pygame.image.fromstring(self.texture.tobytes(), self.texture.size, 'RGBA'), (self.x, self.y))

    def set_texture(self):
        """Load and scale Cactus's texture."""
        # path = os.path.join('assets/images/cactus.png')
        self.texture = assets['cloud']#pygame.image.load(path)
        # self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

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
        self.type="Cactus"
        self.width = 34
        self.height = 44
        self.x = x
        self.y = 110
        self.set_texture()
        self.show()

    def update(self, dx):
        """Update Cactus's position."""
        self.x += dx

    def show(self):
        """Display Cactus."""
        # screen.blit(self.texture, (self.x, self.y))
        screen.blit(pygame.image.fromstring(self.texture.tobytes(), self.texture.size, 'RGBA'), (self.x, self.y))

    def set_texture(self):
        """Load and scale Cactus's texture."""
        # path = os.path.join('assets/images/cactus.png')
        self.texture = assets[f'obstacle{random.randint(1, 6)}']#pygame.image.load(path)
        # self.texture = pygame.transform.scale(self.texture, (self.width, self.height))


class Collision:
    """
    Class handling collision detection.

    Methods:
    - between(obj1, obj2): Check if two objects collide.
    """

    def between(self, obj1, obj2):
        """Check if two objects collide."""
        distance = math.sqrt((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2)
        if not obj1.ducking and obj2.type=="Cactus":
            return distance < 38
        elif obj1.ducking and obj2.type=="Cactus":
            return distance<45
        elif not obj1.ducking and obj2.type=="Bird"  and obj2.texture_num==0:
            return distance < 35
        elif obj1.ducking and obj2.type=="Bird" and obj2.texture_num==0:
            return distance<35
        elif not obj1.ducking and obj2.type=="Bird"  and obj2.texture_num==1:
            return distance < 30
        elif obj1.ducking and obj2.type=="Bird" and obj2.texture_num==1:
            return distance<32
        else:
            return distance<35


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
        self.clouds = []
        self.collision = Collision()
        self.score = Score(hs)
        self.speed = 4
        self.playing = False
        self.set_sound()
        self.set_labels()
        #self.spawn_cactus()

    def set_labels(self):
        """Load fonts and labels for game over screen."""
        big_font = pygame.font.SysFont('monospace', 24, bold=True)
        small_font = pygame.font.SysFont('monospace', 18)
        self.big_lbl = big_font.render('G A M E  O V E R', 1, (0, 0, 0))
        self.small_lbl = small_font.render('press r to restart', 1, (0, 0, 0))

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
    
    def tospawnclouds(self, loops):
        """Determine if an obstacle should spawn."""
        return loops % 50 == 0

    def spawn_cloud(self):
        """Spawn a new cloud obstacle."""
        if len(self.clouds) > 0:
            prev_cloud = self.clouds[-1]
            x = random.randint(prev_cloud.x + self.dino.width + WIDTH, WIDTH + prev_cloud.x + self.dino.width + 200)
        else:
            x = random.randint(WIDTH + 100, 1000)
        cloud = Cloud(x)
        self.clouds.append(cloud)
        
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
    
    def spawn_Bird(self):
        """Spawn a new bird obstacle."""
        # list with bird
        if len(self.obstacles) > 0:
            prev_obstacle = self.obstacles[-1]
            x = random.randint(prev_obstacle.x + self.dino.width + 84,
                               WIDTH + prev_obstacle.x + self.dino.width + 84)

        # empty list
        else:
            x = random.randint(WIDTH + 100, 1000)

        # create the new cactus
        bird = Bird(x)
        self.obstacles.append(bird)
    
    def spawn_obstacle(self):
        """Spawn a new obstacle (cactus or bird)."""
        if len(self.obstacles) > 0:
            prev_obstacle = self.obstacles[-1]
            x = random.randint(prev_obstacle.x + self.dino.width + 120,WIDTH + prev_obstacle.x + self.dino.width + 120)
            print(prev_obstacle.x,x)
        else:
            x = random.randint(WIDTH + 100, 1000)
        
        if random.random() < 0.8:  # 50% chance of spawning a cactus
            obstacle = Cactus(x)
        else:
            obstacle = Bird(x)
        
        self.obstacles.append(obstacle)
   

    def restart(self):
        """Restart the game."""
        self.__init__(hs=self.score.hs)


def main():
    """Main game loop."""

    # objects
    game = Game()
    dino = game.dino
    
    # variables
    clock = pygame.time.Clock()
    loops = 0
    over = False

    # main loop
    while True:

        if game.playing:

            loops += 1
            
            screen.fill((255,255,255))

            # --- BG ---
            for bg in game.bg:
                bg.update(-game.speed)
                bg.show()
            
            # --- dino ---
            dino.update(loops)
            dino.show()

            # --- cactus ---
            if game.tospawnclouds(loops):
                game.spawn_cloud()
            
            for cloud in game.clouds:
                cloud.update(-game.speed)
                cloud.show()

            # --- cactus ---
            if game.tospawn(loops):
                # game.spawn_cactus()
                # game.spawn_Bird()
                game.spawn_obstacle()

            for cactus in game.obstacles:
                cactus.update(-game.speed)
                if cactus.type=="Bird":
                    cactus.update_fly(loops)
                cactus.show()

                # collision
                if game.collision.between(dino, cactus):
                    over = True


            if over:
                game.over()

            # -- score ---
            game.score.update(loops)
            game.score.show()
            
            
            pygame.display.update()

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if not over:
                        if dino.onground:
                            dino.jump()
                        if not game.playing:
                            game.start()

                elif event.key == pygame.K_DOWN:
                    if not over:
                        if dino.onground:
                            dino.duck()
                
                        if not game.playing:
                            game.start()

                if event.key == pygame.K_r:
                    game.restart()
                    dino = game.dino
                    loops = 0
                    over = False
                    screen.fill((255,255,255))
                    

                    # --- BG ---
                    for bg in game.bg:
                        bg.update(-game.speed)
                        bg.show()
                    dino.show()
                    game.score.show()


            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    if not over:
                        if dino.onground:
                            dino.duckrelease()
                

        pygame.display.update()
        clock.tick(100)

if __name__ == "__main__":
    main()