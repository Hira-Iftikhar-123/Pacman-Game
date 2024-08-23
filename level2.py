import pygame  
import math
import copy
from game_board import boards_level2
from pygame import mixer

#def start_level2():
    #global variables for my game
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load('gallery/sounds/pacman_chomp.wav')
pygame.mixer.music.play(-1, 0.2)

pygame.display.set_caption('PACMAN game by Hira Iftikhar')
FPS = 60
SCREENWIDTH = 650
SCREENHEIGHT = 700
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
FPS_CLOCK = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf',20)
level = copy.deepcopy(boards_level2)
color = 'red'
PI = math.pi
GAME_IMAGES = []
GAME_SOUNDS = []
player_x = 290
player_y = 120
direction = 0
count = 0
score = 0
speed = 2
flicker = False
# right,left,up,down
valid_turns = [False,False,False,False]
direction_command = 0
powerup = False
powerup_counter = 0
eaten_ghost = [False,False,False,False]
moving = False
startup_count = 0
pacman_lives = 3
game_over = False
game_won = False
for i in range (1,5):
    image_path = f'gallery/pics/{i}.png'
    GAME_IMAGES.append(pygame.transform.scale(pygame.image.load(image_path),(28,28)))
#(30, 30) tuple is used to uniformly resize all the images to 30 pixels by 30 pixels,
# maintaining consistency in the dimensions of the images used in the game.
RED_GHOST = pygame.transform.scale(pygame.image.load('gallery/pics/red.png'),(30,30))
PINK_GHOST = pygame.transform.scale(pygame.image.load('gallery/pics/pink.png'),((30,30)))
BLUE_GHOST = pygame.transform.scale(pygame.image.load('gallery/pics/blue.png'),(30,30))
ORANGE_GHOST = pygame.transform.scale(pygame.image.load('gallery/pics/orange.png'),(30,30))
SPOOKY_GHOST = pygame.transform.scale(pygame.image.load('gallery/pics/powerup.png'),(30,30))
DEAD_GHOST = pygame.transform.scale(pygame.image.load('gallery/pics/dead.png'),(30,30))

red_x = 40
red_y = 45
red_direction = 0 # the direction is towards right for red ghost 
pink_x = 210
pink_y = 280
pink_direction = 2 # direction of going up
blue_x = 270
blue_y = 300
blue_direction = 2
orange_x = 300
orange_y = 318
orange_direction = 2
targets = [(player_x,player_y),(player_x,player_y),(player_x,player_y),(player_x,player_y)] # following the player
red_dead = False
pink_dead = False
blue_dead = False
orange_dead = False
red_box = False
pink_box = False
blue_box = False
orange_box = False
ghost_speed = [2,2,2,2]

class Ghost:
    def __init__(self, x_coordinate, y_coordinate, target, speed, direction, img, dead, box, ID):
        self.x_pos = x_coordinate
        self.y_pos = y_coordinate
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 15
        self.targets = target
        self.ghost_speed = speed
        self.direction = direction
        self.img = img
        self.dead = dead        
        self.in_box = box
        self.ID = ID
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        #drawing a rectangle around a ghost square to see when we collide with player   
        if (not powerup and not self.dead) or (eaten_ghost[self.ID] and powerup and not self.dead):
            SCREEN.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.ID]:
            SCREEN.blit(SPOOKY_GHOST, (self.x_pos, self.y_pos))
        else:
            SCREEN.blit(DEAD_GHOST, (self.x_pos, self.y_pos))
            
        ghost_rect = pygame.rect.Rect((self.center_x - 20, self.center_y - 14), (25,25))# len,width
        
        return ghost_rect
    
    def check_collisions(self):
        # right, left , up , down
        num1 = ((SCREENHEIGHT - 50) // 32)
        num2 = (SCREENWIDTH // 30)
        num3 = 15
        self.turns = [False, False, False, False]
        
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 8 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 8 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 2 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 4 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True

        if 210 < self.x_pos < 310 and 260 < self.y_pos < 330:
            self.in_box = True
        else:
            self.in_box = False

        return self.turns, self.in_box

    def red_movement(self):
    # right, left, up, down
        # red will turn when collides with a wall, otherwise it will keep going
        if self.direction == 0:
            if self.targets[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.ghost_speed
            elif not self.turns[0]:
                # target is below me
                if self.targets[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                    #target is above me
                elif self.targets[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                    # target is on right
                elif self.targets[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                    # if i can't find player at right :-)
            elif self.turns[0]:
                self.x_pos += self.ghost_speed              
        elif self.direction == 1:
            if self.targets[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.ghost_speed
            elif not self.turns[1]:
                if self.targets[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                elif self.targets[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                elif self.targets[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
            elif self.turns[1]:
                self.x_pos -= self.ghost_speed
        elif self.direction == 2:
            if self.targets[1] < self.y_pos and self.turns[2]:
                # self.direction = 2
                self.y_pos -= self.ghost_speed
            elif not self.turns[2]:
                if self.targets[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
                elif self.targets[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                elif self.targets[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
            elif self.turns[2]:
                self.y_pos -= self.ghost_speed
        elif self.direction == 3:
            if self.targets[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.ghost_speed
            elif not self.turns[3]:
                if self.targets[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
                elif self.targets[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                elif self.turns[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
            elif self.turns[3]:
                self.y_pos += self.ghost_speed

        if self.x_pos < -30:
            self.x_pos = SCREENWIDTH
        elif self.x_pos > SCREENWIDTH:
            self.x_pos = -30
            
        return self.x_pos, self.y_pos, self.direction
    
    def pink_movement(self):
    # right, left, up, down
        #blue turn left or right at any point, but up or down only with it collides with a wall
        if self.direction == 0:
            if self.targets[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.ghost_speed
            elif not self.turns[0]:
                # target is below me
                if self.targets[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                    #target is above me
                elif self.targets[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                    # target is on right
                elif self.targets[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                    # if i can't find player at right :-)
            elif self.turns[0]:
                self.x_pos += self.ghost_speed
        elif self.direction == 1:
            if self.targets[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.targets[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.ghost_speed
            elif not self.turns[1]:
                if self.targets[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                elif self.targets[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                elif self.targets[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
            elif self.turns[1]:
                self.x_pos -= self.ghost_speed
        elif self.direction == 2:
            if self.targets[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.ghost_speed
            elif self.targets[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.ghost_speed
            elif not self.turns[2]:
                if self.targets[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
                elif self.targets[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                elif self.targets[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
            elif self.turns[2]:
                if self.targets[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
                elif self.targets[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                else:
                    self.y_pos -= self.ghost_speed
        elif self.direction == 3:
            if self.targets[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.ghost_speed
            elif not self.turns[3]:
                if self.targets[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
                elif self.targets[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                elif self.turns[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
            elif self.turns[3]:
                if self.targets[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
                elif self.targets[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                else:
                    self.y_pos += self.ghost_speed

        if self.x_pos < -30:
            self.x_pos = SCREENWIDTH
        elif self.x_pos > SCREENWIDTH:
            self.x_pos = -30
            
        return self.x_pos, self.y_pos, self.direction
    
    def blue_movement(self):
    # right, left, up, down
        # blue turn up or down at any point, but left and right only with it collides with a wall
        if self.direction == 0:
            if self.targets[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.ghost_speed
            elif not self.turns[0]:
                # target is below me
                if self.targets[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                    #target is above me
                elif self.targets[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                    # target is on right
                elif self.targets[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                    # if i can't find player at right :-)
            elif self.turns[0]:
                if self.targets[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                if self.targets[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                else:
                    self.x_pos += self.ghost_speed
        elif self.direction == 1:
            if self.targets[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.targets[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.ghost_speed
            elif not self.turns[1]:
                if self.targets[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                elif self.targets[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                elif self.targets[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
            elif self.turns[1]:
                if self.targets[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                if self.targets[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                else:
                    self.x_pos -= self.ghost_speed
        elif self.direction == 2:
            if self.targets[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.ghost_speed
            elif not self.turns[2]:
                if self.targets[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
                elif self.targets[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                elif self.targets[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
            elif self.turns[2]:
                self.y_pos -= self.ghost_speed
        elif self.direction == 3:
            if self.targets[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.ghost_speed
            elif not self.turns[3]:
                if self.targets[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
                elif self.targets[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                elif self.turns[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
            elif self.turns[3]:
                self.y_pos += self.ghost_speed

        if self.x_pos < -30:
            self.x_pos = SCREENWIDTH
        elif self.x_pos > SCREENWIDTH:
            self.x_pos = -30
            
        return self.x_pos, self.y_pos, self.direction
    
    def orange_movement(self):
    # right, left, up, down
        # orange ghost will turn when he collides and keep following player
        if self.direction == 0:
            if self.targets[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.ghost_speed
            elif not self.turns[0]:
                # target is below me
                if self.targets[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                    #target is above me
                elif self.targets[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                    # target is on right
                elif self.targets[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                    # if i can't find player at right :-)
            elif self.turns[0]:
                if self.targets[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                if self.targets[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                else:
                    self.x_pos += self.ghost_speed
        elif self.direction == 1:
            if self.targets[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.targets[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.ghost_speed
            elif not self.turns[1]:
                if self.targets[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                elif self.targets[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                elif self.targets[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
            elif self.turns[1]:
                if self.targets[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                if self.targets[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                else:
                    self.x_pos -= self.ghost_speed
        elif self.direction == 2:
            if self.targets[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.ghost_speed
            elif self.targets[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.ghost_speed
            elif not self.turns[2]:
                if self.targets[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
                elif self.targets[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                elif self.targets[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.ghost_speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
            elif self.turns[2]:
                if self.targets[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
                elif self.targets[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                else:
                    self.y_pos -= self.ghost_speed
        elif self.direction == 3:
            if self.targets[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.ghost_speed
            elif not self.turns[3]:
                if self.targets[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
                elif self.targets[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                elif self.turns[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.ghost_speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
            elif self.turns[3]:
                if self.targets[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.ghost_speed
                elif self.targets[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.ghost_speed
                else:
                    self.y_pos += self.ghost_speed

        if self.x_pos < -30:
            self.x_pos = SCREENWIDTH
        elif self.x_pos > SCREENWIDTH:
            self.x_pos = -30
            
        return self.x_pos, self.y_pos, self.direction
    
def the_game_board(lvl):
    
    # GAME_SOUNDS['beginning'].play()
    
    num1 = ((SCREENHEIGHT - 50) // 32) # the // are used for floor division to get ans in int, 32 is vertical height of pacman game board                               
    num2 = (SCREENWIDTH//30)           # 30 is the horizontal length of pacman game board
    
    # nested loops for dealing/moving within the board
    for i in range (len(lvl)):
        for j in range (len(lvl[i])):
            if lvl[i][j] == 1:
                pygame.draw.circle(SCREEN,'white',(j * num2 + (0.5 * num2),i * num1 + (0.5 * num1)),3)
            if lvl[i][j] == 2 and not flicker:
                pygame.draw.circle(SCREEN,'white',(j * num2 + (0.5 * num2),i * num1 + (0.5 * num1)),9)
            if lvl[i][j] == 3:
                pygame.draw.line(SCREEN,color,(j * num2 + (0.5 * num2), (i*num1)),(j * num2 + (0.5 * num2), ((i*num1) + num1)),2)
            if lvl[i][j] == 4:
                pygame.draw.line(SCREEN,color,(j * num2,i * num1 + (0.5 * num1)),(j * num2 + num2,i * num1 + (0.5 * num1)),2)
            if lvl[i][j] == 5:
                pygame.draw.arc(SCREEN,color,[(j * num2 - (num2 * 0.25)) - 3, (i * num1 + (0.5 * num1)),num1,num2],0,(PI/2),2)
            if lvl[i][j] == 6:
                pygame.draw.arc(SCREEN,color,[(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)),num1,num2],(PI/2),PI,2)
            if lvl[i][j] == 7:
                pygame.draw.arc(SCREEN,color,[(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)),num1,num2],PI,(3*(PI/2)),2)
            if lvl[i][j] == 8:
                pygame.draw.arc(SCREEN,color,[(j * num2 - (num2 * 0.3)) - 2, (i * num1 - (0.4 * num1)),num1,num2],(3*(PI/2)),2*PI,2)
            if lvl[i][j] == 9:
                pygame.draw.line(SCREEN,'white',(j * num2,i * num1 + (0.5 * num1)),(j * num2 + num2,i * num1 + (0.5 * num1)),2)

def game_player():
    if direction == 0:
        SCREEN.blit(GAME_IMAGES[count // 5] , (player_x,player_y))
    elif direction == 1:
        SCREEN.blit(pygame.transform.flip(GAME_IMAGES[count // 5],True,False), (player_x,player_y))
    elif direction == 2:
        SCREEN.blit(pygame.transform.rotate(GAME_IMAGES[count // 5],90), (player_x,player_y))
    elif direction == 3:
        SCREEN.blit(pygame.transform.rotate(GAME_IMAGES[count // 5],270), (player_x,player_y))
    
def check_movement(centerx, centery):
    turns = [False, False, False, False]
    num1 = (SCREENHEIGHT - 50) // 32        #how tall each piece is
    num2 = (SCREENWIDTH // 30)              #how wide each piece is
    num3 = 15
    
    # check collisions of player based on center of player image +/- fudge factor
    if 0 < centerx // 30 < 29:
        #these 4 directions are for left,right,up and down
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                # print(centery // num1)
                # print(center_x//num2)
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 4 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 4 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 4 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 4 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True
    return turns

def move_player(play_x, play_y):
    # right, left, up, down
    if direction == 0 and valid_turns[0]:
        play_x += speed
    elif direction == 1 and valid_turns[1]:
        play_x -= speed
    if direction == 2 and valid_turns[2]:
        play_y -= speed
    elif direction == 3 and valid_turns[3]:
        play_y += speed
        
    if play_x > 650:
        play_x = -47
    elif play_x < -50:
        play_x = 647
    return play_x, play_y

def get_target(redg,pinkg,blueg,orangeg):
    
        if player_x < 325:
            runaway_x = 650
        else:
            runaway_x = 0

        if player_y < 325:
            runaway_y = 650
        else:
            runaway_y = 0

        return_target = (250,300)  # back to the box

        if powerup:
            if not redg.dead and not eaten_ghost[0]:
                red_target = (runaway_x, runaway_y)
            elif not redg.dead and eaten_ghost[0]:
                if redg.in_box:
                    red_target = (275, 100)
                else:
                    red_target = (player_x, player_y)
            else:
                red_target = return_target

            if not pinkg.dead:
                pink_target = (runaway_x, player_y)
            elif not pinkg.dead and eaten_ghost[1]:
                if pinkg.in_box:
                    pink_target = (275, 100)
                else:
                    red_target = (player_x, player_y)
            else:
                pink_target = return_target

            if not blueg.dead:
                blue_target = (player_x, runaway_y)
            elif not blueg.dead and eaten_ghost[2]:
                if blueg.in_box:
                    blue_target = (275, 100)
            else:
                blue_target = return_target

            if not orangeg.dead: 
                orange_target = (325, 325)
            elif not orangeg.dead and eaten_ghost[3]:
                if orangeg.in_box:
                    orange_target = (275, 100)
            else:
                orange_target = return_target

        else:
            if not redg.dead:
                if redg.in_box:
                    red_target = (275, 100)
                else:
                    red_target = (player_x, player_y)
            else:
                red_target = return_target

            if not pinkg.dead:
                if pinkg.in_box:
                    pink_target = (275, 100)
                else:
                    pink_target = (player_x, player_y)
            else:
                pink_target = return_target

            if not blueg.dead:
                if blueg.in_box:
                    blue_target = (275, 100)
                else:
                    blue_target = (player_x, player_y)
            else:
                blue_target = return_target

            if not orangeg.dead:
                if orangeg.in_box:
                    orange_target = (275, 100)
                else:
                    orange_target = (player_x, player_y)
            else:
                orange_target = return_target

        return [red_target, pink_target, blue_target, orange_target]

def draw_footer():
    score_text = font.render(f'Score: {score}',True,'white')
    SCREEN.blit(score_text,(8,670))
    if powerup:
        pygame.draw.circle(SCREEN, 'blue', (140, 680), 15)
    for i in range(pacman_lives):
        SCREEN.blit(pygame.transform.scale(GAME_IMAGES[0], (25, 25)), (520 + i * 40, 665))
    if game_over:
        pygame.draw.rect(SCREEN,'grey',[20,160,620,260],0,10)
        pygame.draw.rect(SCREEN,'white',[40,180,580,220],0,10)
        game_over_text = font.render('Game Over! Press Space to restart',True,'red')
        SCREEN.blit(game_over_text,(70,300))
    if game_won:
        pygame.draw.rect(SCREEN,'white',[20,160,620,260],0,10)
        pygame.draw.rect(SCREEN,'white',[40,180,580,220],0,10)
        game_over_text = font.render('Game Won! Press Space to restart',True,'green')
        SCREEN.blit(game_over_text,(70,300))     
        
def pacman_score(player_score,power, power_up_count,eaten_ghosts):

    num1 = (SCREENHEIGHT - 50) // 32
    num2 = (SCREENWIDTH // 30)

    if player_x > 0 and player_x < 647:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            eatfruit_sound = mixer.Sound('gallery\sounds\pacman_eatfruit.wav')
            eatfruit_sound.play()
            player_score += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            eat_fruit_sound = mixer.Sound('gallery\sounds\pacman_eatfruit.wav')
            eat_fruit_sound.play()
            player_score += 30
            power = True
            power_up_count = 0
            eaten_ghosts = [False,False,False,False]
        if player_score >= 10000:
            pacman_extrapac = mixer.Sound('gallery/sounds/pacman_extrapac.wav')
            pacman_extrapac.play()
    return player_score,power, power_up_count,eaten_ghosts

# main code running
running = True
while running:
    FPS_CLOCK.tick(FPS)
    if count < 19:
        count += 1
        if count > 5:
            flicker = False
    else:
        count = 0
        flicker = True
    
    if powerup and powerup_counter <= 600:
        powerup_counter += 1
    elif powerup and powerup_counter > 600:
        powerup_counter = 0
        powerup = False
        eaten_ghost = [False,False,False,False]
        
    if startup_count < 250 and not game_over and not game_won:
        moving = False
        startup_count += 1
    else:
        moving = True
    
    SCREEN.fill('black')
    text = font.render("Level 2", True, (255, 255, 255))  
    SCREEN.blit(text, (SCREEN.get_width() // 2 - text.get_width() // 2, SCREEN.get_height() // 1.9 - text.get_height() // 3))

    the_game_board(level)        
    center_x = player_x + 16
    center_y = player_y + 14
    
    player_circle = pygame.draw.circle(SCREEN,'black',(center_x ,center_y ),16,2)

    game_player()
    draw_footer()
    valid_turns = check_movement(center_x, center_y)

    red = Ghost(red_x, red_y, targets[0], ghost_speed[0], red_direction, RED_GHOST, red_dead, red_box, 0)
    pink = Ghost(pink_x, pink_y, targets[1], ghost_speed[1], pink_direction,PINK_GHOST, pink_dead,pink_box, 1)
    blue = Ghost(blue_x, blue_y, targets[2], ghost_speed[2], blue_direction,BLUE_GHOST, blue_dead,blue_box, 2)
    orange = Ghost(orange_x, orange_y, targets[3], ghost_speed[3], orange_direction,ORANGE_GHOST, orange_dead,orange_box, 3)
    targets = get_target(red,pink,blue,orange) #a function to handle the different targets for the ghosts

    if moving:
            player_x, player_y = move_player(player_x,player_y)
            if not red_dead and not red.in_box:
                red_x, red_y ,red_direction = red.red_movement()
            else:
                red_x, red_y ,red_direction = red.orange_movement()
            if not pink_dead and not pink.in_box:
                pink_x, pink_y ,pink_direction = pink.pink_movement()
            else:
                pink_x, pink_y ,pink_direction = pink.orange_movement()
            if not blue_dead and not blue.in_box:
                blue_x, blue_y ,blue_direction = blue.blue_movement()
            else:
                blue_x, blue_y ,blue_direction = blue.orange_movement()
            orange_x, orange_y ,orange_direction = orange.orange_movement()

    if powerup:
        ghost_speed = [1,1,1,1]
    else:
        ghost_speed = [2,2,2,2]
        
    if eaten_ghost[0]:
        ghost_speed[0] = 2
    if eaten_ghost[1]:
        ghost_speed[1] = 2
    if eaten_ghost[2]:
        ghost_speed[2] = 2
    if eaten_ghost[3]:
        ghost_speed[3] = 2
    if red_dead:
        ghost_speed[0] = 4
    if pink_dead:
        ghost_speed[1] = 4
    if blue_dead:
        ghost_speed[2] = 4
    if orange_dead:
        ghost_speed[3] = 4
    
    game_won = True
    for i in range (len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False
    
    score,powerup, powerup_counter,eaten_ghost  = pacman_score(score,powerup, powerup_counter,eaten_ghost)
    
    if not powerup:
        if (player_circle.colliderect(red.rect) and not red.dead) or (player_circle.colliderect(pink.rect) and not pink.dead) or \
            (player_circle.colliderect(blue.rect) and not blue.dead) or (player_circle.colliderect(orange.rect) and not orange.dead):
            if pacman_lives > 0:
                pacman_lives -= 1
                startup_count = 0
                powerup = False
                power_counter = 0
                player_x = 290
                player_y = 120
                direction = 0
                direction_command = 0
                red_x = 40
                red_y = 45
                red_direction = 0 
                pink_x = 320
                pink_y = 235
                pink_direction = 2
                blue_x = 270
                blue_y = 300
                blue_direction = 2
                orange_x = 300
                orange_y = 318
                orange_direction = 2
                eaten_ghost = [False, False, False, False]
                red_dead = False
                pink_dead = False
                blue_dead = False
                orange_dead = False
                pacman_dead = pygame.mixer.Sound('gallery/sounds/pacman_death.wav')
                pacman_dead.play()
                pygame.time.delay(1000)
            else:
                moving = False
                game_over = True
                startup_count = 0
    
    if powerup and player_circle.colliderect(red.rect) and eaten_ghost[0] and not red.dead:
        if pacman_lives > 0:
            pacman_lives -= 1
            startup_count = 0
            powerup = False
            power_counter = 0
            player_x = 290
            player_y = 120
            direction = 0
            direction_command = 0
            red_x = 40
            red_y = 45
            red_direction = 0  
            pink_x = 320
            pink_y = 235
            pink_direction = 2 
            blue_x = 270
            blue_y = 300
            blue_direction = 2
            orange_x = 300
            orange_y = 318
            orange_direction = 2
            eaten_ghost = [False, False, False, False]
            red_dead = False
            pink_dead = False
            blue_dead = False
            orange_dead = False
            pacman_dead = pygame.mixer.Sound('gallery/sounds/pacman_death.wav')
            pacman_dead.play()
            pygame.time.delay(1000)
        else:
            moving = False
            game_over = True
            startup_count = 0
    if powerup and player_circle.colliderect(pink.rect) and eaten_ghost[1] and not pink.dead:
        if pacman_lives > 0:
                pacman_lives -= 1
                startup_count = 0
                powerup = False
                power_counter = 0
                player_x = 290
                player_y = 120
                direction = 0
                direction_command = 0
                red_x = 40
                red_y = 45
                red_direction = 0 
                pink_x = 320
                pink_y = 235
                pink_direction = 2 
                blue_x = 270
                blue_y = 300
                blue_direction = 2
                orange_x = 300
                orange_y = 318
                orange_direction = 2
                eaten_ghost = [False, False, False, False]
                red_dead = False
                pink_dead = False
                blue_dead = False
                orange_dead = False
                pacman_dead = pygame.mixer.Sound('gallery/sounds/pacman_death.wav')
                pacman_dead.play()
                pygame.time.delay(1000)
        else:
            moving = False
            game_over = True
            startup_count = 0
    if powerup and player_circle.colliderect(blue.rect) and eaten_ghost[2] and not blue.dead:
        if pacman_lives > 0:
                pacman_lives -= 1
                startup_count = 0
                powerup = False
                power_counter = 0
                player_x = 290
                player_y = 120
                direction = 0
                direction_command = 0
                red_x = 40
                red_y = 45
                red_direction = 0 # the direction is towards right for red ghost 
                pink_x = 320
                pink_y = 235
                pink_direction = 2 # direction of going up
                blue_x = 270
                blue_y = 300
                blue_direction = 2
                orange_x = 300
                orange_y = 318
                orange_direction = 2
                eaten_ghost = [False, False, False, False]
                red_dead = False
                pink_dead = False
                blue_dead = False
                orange_dead = False
                pacman_dead = pygame.mixer.Sound('gallery/sounds/pacman_death.wav')
                pacman_dead.play()
                pygame.time.delay(1000)
        else:
            moving = False
            game_over = True
            startup_count = 0
    if powerup and player_circle.colliderect(orange.rect) and eaten_ghost[3] and not orange.dead:
        if pacman_lives > 0:
            pacman_lives -= 1
            startup_count = 0
            powerup = False
            power_counter = 0
            player_x = 290
            player_y = 120
            direction = 0
            direction_command = 0
            red_x = 40
            red_y = 45
            red_direction = 0 
            pink_x = 320
            pink_y = 235
            pink_direction = 2 
            blue_x = 270
            blue_y = 300
            blue_direction = 2
            orange_x = 300
            orange_y = 318
            orange_direction = 2
            eaten_ghost = [False, False, False, False]
            red_dead = False
            pink_dead = False
            blue_dead = False
            orange_dead = False  
            pacman_dead = pygame.mixer.Sound('gallery/sounds/pacman_death.wav')
            pacman_dead.play()
            pygame.time.delay(1000)
        else:
            moving = False
            game_over = True
            startup_count = 0
    
    if powerup and player_circle.colliderect(red.rect) and not red.dead and not eaten_ghost[0]:
        pacman_eat_ghost1 = mixer.Sound('gallery/sounds/pacman_eatghost.wav')
        pacman_eat_ghost1.play()
        red_dead = True
        eaten_ghost[0] = True
        score +=  2 ** eaten_ghost.count(True) * 100
    if powerup and player_circle.colliderect(pink.rect) and not pink.dead and not eaten_ghost[1]:
        pacman_eat_ghost2 = mixer.Sound('gallery/sounds/pacman_eatghost.wav')
        pacman_eat_ghost2.play()
        pink_dead = True
        eaten_ghost[1] = True
        score +=  2 ** eaten_ghost.count(True) * 100
    if powerup and player_circle.colliderect(blue.rect) and not blue.dead and not eaten_ghost[2]:
        pacman_eat_ghost3 = mixer.Sound('gallery/sounds/pacman_eatghost.wav')
        pacman_eat_ghost3.play()
        blue_dead = True
        eaten_ghost[2] = True
        score +=  2 ** eaten_ghost.count(True) * 100
    if powerup and player_circle.colliderect(orange.rect) and not orange.dead and not eaten_ghost[3]:
        pacman_eat_ghost4 = mixer.Sound('gallery/sounds/pacman_eatghost.wav')
        pacman_eat_ghost4.play()
        orange_dead = True
        eaten_ghost[3] = True
        score +=  2 ** eaten_ghost.count(True) * 100

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # pacman_dead = pygame.mixer.Sound('gallery/sounds/pacman_death.wav') 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3  
            if event.key == pygame.K_SPACE and (game_over or game_won):
                pacman_lives -= 1
                startup_count = 0
                powerup = False
                power_counter = 0
                player_x = 290
                player_y = 120
                direction = 0
                direction_command = 0
                red_x = 40
                red_y = 45
                red_direction = 0  
                pink_x = 320
                pink_y = 235
                pink_direction = 2 
                blue_x = 270
                blue_y = 300
                blue_direction = 2
                orange_x = 300
                orange_y = 318
                orange_direction = 2
                eaten_ghost = [False, False, False, False]
                red_dead = False
                pink_dead = False
                blue_dead = False
                orange_dead = False
                score = 0
                pacman_lives = 3
                level = copy.deepcopy(boards_level2) 
                game_over = False
                game_won = False 

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction
                        
    if direction_command == 0 and valid_turns[0]:
        direction = 0
    if direction_command == 1 and valid_turns[1]:
        direction = 1
    if direction_command == 2 and valid_turns[2]:
        direction = 2
    if direction_command == 3 and valid_turns[3]:
        direction = 3
    
    if red.in_box and red_dead:
        red_dead = False 
    if pink.in_box and pink_dead:
        pink_dead = False
    if blue.in_box and blue_dead:
        blue_dead = False
    if orange.in_box and orange_dead:
        orange_dead = False
        
    pygame.display.flip()
pygame.quit()

    

    