'''

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

Gregory Clarke
Advanced Computer Programing
5/24/2019

Version 1.0

'''

import pygame, sys, random, math
import pygame as pg
from pygame.locals import *

backgroundc = (0, 0, 0)
entity_color = (255, 255, 255)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
RED = (255, 0, 0)


class Entity(pygame.sprite.Sprite):
    """Inherited by any object in the game."""

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # This makes a rectangle around the entity, used for anything
        # from collision to moving around.
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Paddle(Entity):
    """
    Player controlled or AI controlled, main interaction with
    the game
    """

    def __init__(self, x, y, width, height):
        super(Paddle, self).__init__(x, y, width, height)

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(entity_color)


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.BULLET_SPEED = 25

        self.image = pygame.Surface([8, 8])
        self.image.fill(RED)

        self.rect = self.image.get_rect()

        #
        # Position the bullet at the player's current location
        start_x = window_width / 2
        start_y = window_height / 2
        self.floating_point_x = start_x
        self.floating_point_y = start_y

        # Get from the mouse the destination location for the bullet
        pos = pygame.mouse.get_pos()

        dest_x = pos[0]
        dest_y = pos[1]

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Angle the bullet sprite so it doesn't look like it is flying
        # sideways.
        # self.rect.angle = math.degrees(angle)

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        self.change_x = math.cos(angle) * self.BULLET_SPEED
        self.change_y = math.sin(angle) * self.BULLET_SPEED

    def update(self):
        """ Move the bullet. """
        self.floating_point_y += self.change_y
        self.floating_point_x += self.change_x

        # The rect.x and rect.y are converted to integers.
        self.rect.y = int(self.floating_point_y)
        self.rect.x = int(self.floating_point_x)

        # If the bullet flies of the screen, get rid of it.
        if self.rect.x < 0 or self.rect.x > window_width or self.rect.y < 0 or self.rect.y > window_height:
            self.kill()


class Background(pygame.sprite.Sprite):
    def __init__(self, map_type):
        super().__init__()
        self.map_type = map_type
        self.image = pygame.image.load(map_type+".png").convert_alpha()

        self.rect = self.image.get_rect()


class Path(pygame.sprite.Sprite):
    def __init__(self, path_type):
        super().__init__()

        self.image = pygame.image.load(path_type+".png").convert_alpha()

        self.rect = self.image.get_rect()


class Player(Paddle):
    def __init__(self, x, y, width, height, screen_rect):
        super(Player, self).__init__(x, y, width, height)

        # How many pixels the Player Paddle should move on a given frame.
        self.y_change = 0
        self.x_change = 0
        # How many pixels the paddle should move each frame a key is pressed.
        self.x_dist = 20
        self.y_dist = 20

        self.orig_image = pygame.image.load("character.png").convert_alpha()  #
        self.image = self.orig_image
        self.rect = self.image.get_rect(center=screen_rect.center)
        self.angle = 0
        self.distance = 0
        self.angle_offset = 0

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def get_angle(self):
        mouse = pg.mouse.get_pos()
        offset = (self.rect.centerx - mouse[0], self.rect.centery - mouse[1])
        self.angle = math.degrees(math.atan2(*offset)) - self.angle_offset
        old_center = self.rect.center
        self.image = pg.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect(center=old_center)
        self.distance = math.sqrt((offset[0] * offset[0]) + (offset[1] * offset[1]))

    def MoveKeyDown(self, key): #, hitx, hity):
        """Responds to a key-down event and moves accordingly"""

        if key == pygame.K_w:
            self.y_change += -self.y_dist

        elif key == pygame.K_s:
            self.y_change += self.y_dist

        elif key == pygame.K_d:
            self.x_change += self.x_dist

        elif key == pygame.K_a:
            self.x_change += -self.x_dist

    def MoveKeyUp(self, key):
        """Responds to a key-up event and stops movement accordingly"""
        if key == pygame.K_w:
            self.y_change += self.y_dist

        elif key == pygame.K_s:
            self.y_change += -self.y_dist

        elif key == pygame.K_d:
            self.x_change += -self.x_dist

        elif key == pygame.K_a:
            self.x_change += self.x_dist

    def Y_Move(self):

        for ting in background_list:
            if ting != Main:
                ting.rect.move_ip(0, -self.y_change)

        # for ting in path_list:
        #     # if ting != Main:
        #     ting.rect.move_ip(0, -self.y_change)

    def X_Move(self):

        for ting in background_list:
            if ting != Main:
                ting.rect.move_ip(-self.x_change, 0)

        # for ting in path_list:
        #     # if ting != Main:
        #     ting.rect.move_ip(-self.x_change, 0)


    def Borders(self):
        hity = 0
        hitx = 0

        Main.rect.move_ip(-self.x_change, -self.y_change)

        if Main == UP:

            # if Main.rect.y < - map_height / 2 + window_height / 2 - Buffer:
            #     Main.rect.y = - map_height / 2 + window_height / 2 - Buffer
            #     item.rect.y = - map_height / 2 + window_height / 2 - Buffer
            #     hity += 1
            #
            # if Main.rect.x < - map_width / 2 + window_width / 2 - Buffer:
            #     Main.rect.x = - map_width / 2 + window_width / 2 - Buffer
            #     Main.rect.x = - map_width / 2 + window_width / 2 - Buffer
            #     hitx += 1
            #
            # elif Main.rect.x > - map_width / 2 + window_width / 2 + Buffer:
            #     item.rect.x = - map_width / 2 + window_width / 2 + Buffer
            #     hitx += 1

            if hitx == 0:
                self.X_Move()

            if hity == 0:
                self.Y_Move()

        if Main == DOWN:

            # if Main.rect.y > - map_height / 2 + window_height / 2 + Buffer:
            #     Main.rect.y = - map_height / 2 + window_height / 2 + Buffer
            #     hity += 1
            #
            # if Main.rect.x < - map_width / 2 + window_width / 2 - Buffer:
            #     Main.rect.x = - map_width / 2 + window_width / 2 - Buffer
            #     hitx += 1
            #
            # elif Main.rect.x >= - map_width / 2 + window_width / 2 + Buffer:
            #     Main.rect.x = - map_width / 2 + window_width / 2 + Buffer
            #     hitx += 1

            if hitx == 0:
                self.X_Move()

            if hity == 0:
                self.Y_Move()

        if Main == LEFT:

            # if Main.rect.y < - map_height / 2 + window_height / 2 - Buffer:
            #     Main.rect.y = - map_height / 2 + window_height / 2 - Buffer
            #     hity += 1
            #
            # elif Main.rect.y > - map_height / 2 + window_height / 2 + Buffer:
            #     Main.rect.y = - map_height / 2 + window_height / 2 + Buffer
            #     hity += 1
            #
            # if Main.rect.x < - map_width / 2 + window_width / 2 - Buffer:
            #     Main.rect.x = - map_width / 2 + window_width / 2 - Buffer
            #     hitx += 1

            if hitx == 0:
                self.X_Move()

            if hity == 0:
                self.Y_Move()

        if Main == RIGHT:

            # if Main.rect.y < - map_height / 2 + window_height / 2 - Buffer:
            #     Main.rect.y = - map_height / 2 + window_height / 2 - Buffer
            #     hity += 1
            #
            # elif Main.rect.y > - map_height / 2 + window_height / 2 + Buffer:
            #     Main.rect.y = - map_height / 2 + window_height / 2 + Buffer
            #     hity += 1
            #
            # if Main.rect.x > - map_width / 2 + window_width / 2 + Buffer:
            #     Main.rect.x = - map_width / 2 + window_width / 2 + Buffer
            #     hitx += 1

            if hitx == 0:
                self.X_Move()

            if hity == 0:
                self.Y_Move()

        if Main == RIGHT_UP:

            # if Main.rect.y < - map_height / 2 + window_height / 2 - Buffer:
            #     Main.rect.y = - map_height / 2 + window_height / 2 - Buffer  # Bottom Y and Left X
            #     hity += 1
            #
            # if Main.rect.y > - map_height / 2 + window_height / 2 + Buffer:
            #     if Main.rect.x < - map_width / 2 + window_width / 2 - Buffer:
            #         if Main.rect.x - map_width / 2 + window_width / 2 - Buffer:
            #             Main.rect.y = - map_height / 2 + window_height / 2 + Buffer  # Top Y and Right X
            #             hity += 1
            #
            #         if Main.rect.y > - map_height / 2 + window_height / 2 + Buffer + 20:
            #             Main.rect.x = - map_width / 2 + window_width / 2 - Buffer  # Right X
            #             hitx += 1
            #
            # if Main.rect.x > - map_width / 2 + window_width / 2 + Buffer:
            #     Main.rect.x = - map_width / 2 + window_width / 2 + Buffer  # Left X
            #     hitx += 1

            if hitx == 0:
                self.X_Move()

            if hity == 0:
                self.Y_Move()

        if Main == LEFT_UP:
            # XD = - 625 - Main.rect.x
            # YD = - 1008 - Main.rect.y
            #
            # if Main.rect.y < - map_height / 2 + window_height / 2 - Buffer:
            #     Main.rect.y = - map_height / 2 + window_height / 2 - Buffer
            #     hity += 1
            #
            # if Main.rect.y > - map_height / 2 + window_height / 2 + Buffer:
            #     if Main.rect.x > - map_width / 2 + window_width / 2 + Buffer:
            #         if YD >= XD:
            #             Main.rect.y = - map_height / 2 + window_height / 2 + Buffer
            #             hity += 1
            #
            #         if XD > YD:
            #             Main.rect.x = - map_width / 2 + window_width / 2 + Buffer
            #             hitx += 1
            #
            #         # if YD == XD:
            #         #     Main.rect.x = - map_width / 2 + window_width / 2 + Buffer
            #         #     Main.rect.y = - map_height / 2 + window_height / 2 + Buffer
            #         #     hitx += 1
            #         #     hity += 1
            #
            # elif Main.rect.x < - map_width / 2 + window_width / 2 - Buffer:
            #     Main.rect.x = - map_width / 2 + window_width / 2 - Buffer  # Left X
            #     hitx += 1

            if hitx == 0:
                self.X_Move()

            if hity == 0:
                self.Y_Move()

        if Main == RIGHT_DOWN:

            # if Main.rect.y < - map_height / 2 + window_height / 2 - Buffer \
            #         and - map_width / 2 + window_width / 2 - Buffer - player_width > Main.rect.x:
            #     Main.rect.y = - map_height / 2 + window_height / 2 - Buffer  # Bottom Y and Left X
            #     hity += 1
            #
            # elif Main.rect.y > - map_height / 2 + window_height / 2 + Buffer \
            #         and Main.rect.x < - map_width / 2 + window_width / 2 + Buffer + player_width:
            #     Main.rect.y = - map_height / 2 + window_height / 2 + Buffer  # Top Y and Right X
            #     hity += 1
            #
            # if Main.rect.x < - map_width / 2 + window_width / 2 - Buffer \
            #         and Main.rect.y < - map_height / 2 + window_height / 2 - Buffer:
            #     Main.rect.x = - map_width / 2 + window_width / 2 - Buffer  # Right X
            #     hitx += 1
            #
            # elif Main.rect.x > - map_width / 2 + window_width / 2 + Buffer:
            #     Main.rect.x = - map_width / 2 + window_width / 2 + Buffer  # Left X
            #     hitx += 1

            if hitx == 0:
                self.X_Move()

            if hity == 0:
                self.Y_Move()

        if Main == LEFT_DOWN:

            # if Main.rect.y > - map_height / 2 + window_height / 2 + Buffer \
            #         and - map_width / 2 + window_width / 2 - Buffer - player_width < Main.rect.x:
            #     Main.rect.y = - map_height / 2 + window_height / 2 + Buffer  # Bottom Y and Left X
            #     hity += 1
            #
            # elif Main.rect.y < - map_height / 2 + window_height / 2 - Buffer \
            #         and Main.rect.x > - map_width / 2 + window_width / 2 + Buffer + player_width:
            #     Main.rect.y = - map_height / 2 + window_height / 2 - Buffer  # Top Y and Right X
            #     hity += 1
            #
            # if Main.rect.x > - map_width / 2 + window_width / 2 + Buffer \
            #         and Main.rect.y < - map_height / 2 + window_height / 2 - Buffer:
            #     Main.rect.x = - map_width / 2 + window_width / 2 + Buffer  # Right X
            #     hitx += 1
            #
            # elif Main.rect.x < - map_width / 2 + window_width / 2 - Buffer:
            #     Main.rect.x = - map_width / 2 + window_width / 2 - Buffer  # Left X
            #     hitx += 1

            if hitx == 0:
                self.X_Move()

            if hity == 0:
                self.Y_Move()

    def update(self):
        self.Borders()


pygame.init()

window_width = 1750
window_height = 984
map_height = 3000
map_width = 3000
screen = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Unhinged")

clock = pygame.time.Clock()

screen_rect = screen.get_rect()

player_width = 120

active_list = pygame.sprite.Group()
background_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
path_list = pygame.sprite.Group()

fontObj = pygame.font.SysFont('stencil', 32)
fontObj2 = pygame.font.SysFont('Times New Roman', 20)

ExitVar = "Press Escape To Pause"
ExitKey = fontObj2.render(ExitVar, True, GREY)
ExitKeyPos = ExitKey.get_rect()
ExitKeyPos.center = (100, 25)

UpVar = "w"
UpKey = fontObj.render("Up = " + UpVar, True, WHITE)
UpKeyPos = UpKey.get_rect()
UpKeyPos.center = (window_width * .2, 50)

DownVar = "s"
DownKey = fontObj.render("Down = " + DownVar, True, WHITE)
DownKeyPos = UpKey.get_rect()
DownKeyPos.center = (window_width * .4, 50)

LeftVar = "a"
LeftKey = fontObj.render("Left = " + LeftVar, True, WHITE)
LeftKeyPos = UpKey.get_rect()
LeftKeyPos.center = (window_width * .6, 50)

RightVar = "d"
RightKey = fontObj.render("Right = " + RightVar, True, WHITE)
RightKeyPos = UpKey.get_rect()
RightKeyPos.center = (window_width * .8, 50)


homescreen = pygame.image.load("TitleScreen.png").convert_alpha()
homescreenExit = pygame.image.load("ExitSelected.png").convert_alpha()
exposition = pygame.image.load("Exposition.png").convert_alpha()
loading = pygame.image.load("LoadingScreen.png").convert_alpha()
pausescreen = pygame.image.load("PauseMenu.png").convert_alpha()
ContinueSelect = pygame.image.load("ContinueSelect.png").convert_alpha()
ExitToMenu = pygame.image.load("ExitToMenu.png").convert_alpha()
Menu = pygame.image.load("MainMenu.png").convert_alpha()
Start = pygame.image.load("StartSelect.png").convert_alpha()
Quit = pygame.image.load("QuitSelect.png").convert_alpha()

First_Var = 0
PreDir = "UP"
Buffer = 160

"""
pygame.mixer.music.load('Horde.mp3')
pygame.mixer.music.play(-1, 0.0)
"""

GAME = True

START = True
EXPO = False
PAUSE = False
ENDLESS = False
RACES = False
OBJECTIVES = False
DEATH = False
HOME = False

global backgroundDOWN
global backgroundUP
global backgroundLEFT_UP
global backgroundLEFT
global backgroundRIGHT
global backgroundRIGHT_DOWN
global backgroundLEFT_DOWN
global backgroundRIGHT_UP

while GAME:

    if START == True:
        screen.blit(homescreen, (0, 0))

        for event in pygame.event.get():

            if event.type == QUIT:

                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:

                START = False
                #EXPO = True
                HOME = True

            pygame.display.update()

    # if EXPO == True:
    #
    #     screen.blit(exposition, (0, 0))
    #
    #     for event in pygame.event.get():
    #
    #         if event.type == QUIT:
    #
    #             pygame.quit()
    #             sys.exit()
    #
    #         elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
    #
    #             EXPO = False
    #             HOME = True
    #
    #         pygame.display.update()

    if HOME == True:
        screen.blit(Menu, (0, 0))
        mouse_pressed = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()

        #Button Highlights

        if 600 <= pos[0] <= 1150 and 275 <= pos[1] <= 525:
            screen.blit(Start, (0, 0))

        if 600 <= pos[0] <= 1150 and 595 <= pos[1] <= 850:
            screen.blit(Quit, (0, 0))

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN: #Buttons

                if 600 <= pos[0] <= 1150 and 275 <= pos[1] <= 525: #Endless
                    screen.blit(loading, (0, 0))
                    HOME = False
                    ENDLESS = True

                if 600 <= pos[0] <= 1150 and 595 <= pos[1] <= 850: #Exit
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    HOME = False
                    ENDLESS = True

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    if ENDLESS == True:

        if First_Var == 0:  # The first process that runs at the start of the stage

            backgroundDOWN = Background("DOWN")
            backgroundUP = Background("UP")
            backgroundLEFT = Background("LEFT")
            backgroundRIGHT = Background("RIGHT")
            backgroundRIGHT_DOWN = Background("RIGHT-DOWN")
            backgroundRIGHT_UP = Background("RIGHT-UP")
            backgroundLEFT_DOWN = Background("LEFT-DOWN")
            backgroundLEFT_UP = Background("LEFT-UP")

            DOWN = backgroundDOWN
            UP = backgroundUP
            LEFT = backgroundLEFT
            RIGHT = backgroundRIGHT
            RIGHT_DOWN = backgroundRIGHT_DOWN
            RIGHT_UP = backgroundRIGHT_UP
            LEFT_DOWN = backgroundLEFT_DOWN
            LEFT_UP = backgroundLEFT_UP

            #PathUP = Path("PATHUP")
            # PathDOWN = Path("DOWN")
            # PathLEFT = Path("LEFT")
            # PathRIGHT = Path("RIGHT")

            player = Player(window_width / 2 - 60, window_height / 2 - 60, 40, 40, screen_rect)

            chance = random.randint(1, 4)

            if chance == 1:
                Main = backgroundUP

            if chance == 2:
                Main = backgroundDOWN

            if chance == 3:
                Main = backgroundLEFT

            if chance == 4:
                Main = backgroundRIGHT

            Main.rect.move_ip(-(map_width / 2 - window_width / 2), -(map_height / 2 - window_height / 2))

            #path.rect.move_ip(Main.rect.x - map_width / 2 + window_width / 2 + Buffer, Main.rect.y - 1000)
            # Initial Map Creation

            if Main == backgroundUP:
                PreDir = "UP"
                chance = random.randint(1, 2)
                if chance == 1:
                    Next = backgroundRIGHT_DOWN
                    Next.rect.move_ip(Main.rect.x, Main.rect.y - map_height)

                if chance == 2:
                    Next = backgroundLEFT_DOWN
                    Next.rect.move_ip(Main.rect.x, Main.rect.y - map_height)


            if Main == backgroundDOWN:
                PreDir = "DOWN"
                chance = random.randint(1, 2)
                if chance == 1:
                    Next = backgroundRIGHT_UP
                    Next.rect.move_ip(Main.rect.x, Main.rect.y + map_height)


                if chance == 2:
                    Next = backgroundLEFT_UP
                    Next.rect.move_ip(Main.rect.x, Main.rect.y + map_height)

            if Main == backgroundLEFT:
                PreDir = "LEFT"
                chance = random.randint(1, 2)
                if chance == 1:
                    Next = backgroundRIGHT_DOWN
                    Next.rect.move_ip(Main.rect.x - map_width, Main.rect.y)

                if chance == 2:
                    Next = backgroundRIGHT_UP
                    Next.rect.move_ip(Main.rect.x - map_width, Main.rect.y)

            if Main == backgroundRIGHT:
                PreDir = "RIGHT"
                chance = random.randint(1, 2)
                if chance == 1:
                    Next = backgroundLEFT_DOWN
                    Next.rect.move_ip(Main.rect.x + map_width, Main.rect.y)


                if chance == 2:
                    Next = backgroundLEFT_UP
                    Next.rect.move_ip(Main.rect.x + map_width, Main.rect.y)

            #  Adds First Two Chunks and Player on Top
            all_sprites_list.add(Main)
            background_list.add(Main)
            all_sprites_list.add(Next)
            background_list.add(Next)
            #all_sprites_list.add(path)
            #path_list.add(path)
            all_sprites_list.add(player)

            # UPBUTTON = pygame.K_w
            # DOWNBUTTON = pygame.K_s
            # LEFTBUTTON = pygame.K_a
            # RIGHTBUTTON = pygame.K_d
            #
            # button_list = [UPBUTTON, DOWNBUTTON, LEFTBUTTON, LEFTBUTTON]
            #
            # for button in button_list:
            #
            #     chance = random.randint(1, 4)
            #
            #     if chance == 1:
            #         button = backgroundUP
            #
            #     if chance == 2:
            #         Main = backgroundDOWN
            #
            #     if chance == 3:
            #         Main = backgroundLEFT
            #
            #     if chance == 4:
            #         Main = backgroundRIGHT

            First_Var += 1

        #Positioning and Logistics

        for item in background_list:

            inside = 0

            if item.rect.y + map_height > window_height + player_width:
                inside += 1

            if item.rect.y < - player_width:
                inside += 1

            if item.rect.x < - player_width:
                inside += 1

            if item.rect.x + map_width > window_width + player_width:
                inside += 1

            if item != Main:
                if inside == 4:
                    if item.map_type == "RIGHT-DOWN":

                        all_sprites_list.remove(Main)
                        background_list.remove(Main)
                        all_sprites_list.remove(player)
                        chance2 = random.randint(1, 2)

                        if PreDir == "UP":
                            if chance2 == 1:
                                PreDir = "RIGHT"
                                LEFT_UP.rect.x = item.rect.x + map_width
                                LEFT_UP.rect.y = item.rect.y
                                all_sprites_list.add(LEFT_UP)
                                background_list.add(LEFT_UP)
                                all_sprites_list.add(player)

                            if chance2 == 2:
                                PreDir = "RIGHT"
                                LEFT_DOWN.rect.x = item.rect.x + map_width
                                LEFT_DOWN.rect.y = item.rect.y
                                all_sprites_list.add(LEFT_DOWN)
                                background_list.add(LEFT_DOWN)
                                all_sprites_list.add(player)

                        if PreDir == "LEFT":
                            if chance2 == 1:
                                PreDir = "DOWN"
                                LEFT_UP.rect.x = item.rect.x
                                LEFT_UP.rect.y = item.rect.y + map_height
                                all_sprites_list.add(LEFT_UP)
                                background_list.add(LEFT_UP)
                                all_sprites_list.add(player)

                            if chance2 == 2:
                                PreDir = "DOWN"
                                RIGHT_UP.rect.x = item.rect.x
                                RIGHT_UP.rect.y = item.rect.y + map_height
                                all_sprites_list.add(RIGHT_UP)
                                background_list.add(RIGHT_UP)
                                all_sprites_list.add(player)

                    if item.map_type == "LEFT-DOWN":

                        all_sprites_list.remove(Main)
                        background_list.remove(Main)
                        all_sprites_list.remove(player)
                        chance2 = random.randint(1, 2)

                        if PreDir == "UP":
                            if chance2 == 1:
                                PreDir = "LEFT"
                                RIGHT_UP.rect.x = item.rect.x - map_width
                                RIGHT_UP.rect.y = item.rect.y
                                all_sprites_list.add(RIGHT_UP)
                                background_list.add(RIGHT_UP)
                                all_sprites_list.add(player)

                            if chance2 == 2:
                                PreDir = "LEFT"
                                RIGHT_DOWN.rect.x = item.rect.x - map_width
                                RIGHT_DOWN.rect.y = item.rect.y
                                all_sprites_list.add(RIGHT_DOWN)
                                background_list.add(RIGHT_DOWN)
                                all_sprites_list.add(player)

                        if PreDir == "RIGHT":
                            if chance2 == 1:
                                PreDir = "DOWN"
                                LEFT_UP.rect.x = item.rect.x
                                LEFT_UP.rect.y = item.rect.y + map_height
                                all_sprites_list.add(LEFT_UP)
                                background_list.add(LEFT_UP)
                                all_sprites_list.add(player)

                            if chance2 == 2:
                                PreDir = "DOWN"
                                RIGHT_UP.rect.x = item.rect.x
                                RIGHT_UP.rect.y = item.rect.y + map_height
                                all_sprites_list.add(RIGHT_UP)
                                background_list.add(RIGHT_UP)
                                all_sprites_list.add(player)

                    if item.map_type == "RIGHT-UP":
                        all_sprites_list.remove(Main)
                        background_list.remove(Main)
                        all_sprites_list.remove(player)
                        chance2 = random.randint(1, 2)

                        if PreDir == "DOWN":
                            if chance2 == 1:
                                PreDir = "RIGHT"
                                LEFT_UP.rect.x = item.rect.x + map_width
                                LEFT_UP.rect.y = item.rect.y
                                all_sprites_list.add(LEFT_UP)
                                background_list.add(LEFT_UP)
                                all_sprites_list.add(player)

                            if chance2 == 2:
                                PreDir = "RIGHT"
                                LEFT_DOWN.rect.x = item.rect.x + map_width
                                LEFT_DOWN.rect.y = item.rect.y
                                all_sprites_list.add(LEFT_DOWN)
                                background_list.add(LEFT_DOWN)
                                all_sprites_list.add(player)

                        if PreDir == "LEFT":
                            if chance2 == 1:
                                PreDir = "UP"
                                RIGHT_DOWN.rect.x = item.rect.x
                                RIGHT_DOWN.rect.y = item.rect.y - map_height
                                all_sprites_list.add(RIGHT_DOWN)
                                background_list.add(RIGHT_DOWN)
                                all_sprites_list.add(player)

                            if chance2 == 2:
                                PreDir = "UP"
                                LEFT_DOWN.rect.x = item.rect.x
                                LEFT_DOWN.rect.y = item.rect.y - map_height
                                all_sprites_list.add(LEFT_DOWN)
                                background_list.add(LEFT_DOWN)
                                all_sprites_list.add(player)

                    if item.map_type == "LEFT-UP":
                        all_sprites_list.remove(Main)
                        background_list.remove(Main)
                        all_sprites_list.remove(player)
                        chance2 = random.randint(1, 2)

                        if PreDir == "DOWN":
                            if chance2 == 1:
                                PreDir = "LEFT"
                                RIGHT_UP.rect.x = item.rect.x - map_width
                                RIGHT_UP.rect.y = item.rect.y
                                all_sprites_list.add(RIGHT_UP)
                                background_list.add(RIGHT_UP)
                                all_sprites_list.add(player)

                            if chance2 == 2:
                                PreDir = "LEFT"
                                RIGHT_DOWN.rect.x = item.rect.x - map_width
                                RIGHT_DOWN.rect.y = item.rect.y
                                all_sprites_list.add(RIGHT_DOWN)
                                background_list.add(RIGHT_DOWN)
                                all_sprites_list.add(player)

                        if PreDir == "RIGHT":
                            if chance2 == 1:
                                PreDir = "UP"
                                RIGHT_DOWN.rect.x = item.rect.x
                                RIGHT_DOWN.rect.y = item.rect.y - map_height
                                all_sprites_list.add(RIGHT_DOWN)
                                background_list.add(RIGHT_DOWN)
                                all_sprites_list.add(player)

                            if chance2 == 2:
                                PreDir = "UP"
                                LEFT_DOWN.rect.x = item.rect.x
                                LEFT_DOWN.rect.y = item.rect.y - map_height
                                all_sprites_list.add(LEFT_DOWN)
                                background_list.add(LEFT_DOWN)
                                all_sprites_list.add(player)
                    Main = item

        for event in pygame.event.get():

            mouse_pressed = pygame.mouse.get_pressed()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                player.MoveKeyDown(event.key)  #, hitx, hity)

                if event.key == pygame.K_ESCAPE:
                    player.x_change = 0
                    player.y_change = 0
                    ENDLESS = False
                    PAUSE = True

            elif event.type == pygame.KEYUP:
                player.MoveKeyUp(event.key)

        screen.fill((0, 0, 0))
        for ent in all_sprites_list:
            ent.update()

        all_sprites_list.draw(screen)

        screen.blit(UpKey, UpKeyPos)
        screen.blit(DownKey, DownKeyPos)
        screen.blit(LeftKey, LeftKeyPos)
        screen.blit(RightKey, RightKeyPos)
        screen.blit(ExitKey, ExitKeyPos)

        pygame.display.update()
        pygame.display.flip()

        clock.tick(600)

    if PAUSE == True:

        all_sprites_list.draw(screen)
        mouse_pressed = pygame.mouse.get_pressed()
        event_get = pygame.event.get()
        pos = pygame.mouse.get_pos()
        screen.blit(pausescreen, (0, 0))

        # Button Highlights
        if 666 <= pos[0] <= 1088 and 296 <= pos[1] <= 432:
            screen.blit(ContinueSelect, (0, 0))

        if 666 <= pos[0] <= 1088 and 470 <= pos[1] <= 616:
            screen.blit(ExitToMenu, (0, 0))

        for event in event_get:

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # Buttons

                if 666 <= pos[0] <= 1088 and 296 <= pos[1] <= 432:  # Continue
                    # print("yes1")
                    #
                    # for x in event_get:
                    #     print("yes2")
                    #
                    #     if x.type == pygame.KEYDOWN:
                    #         print("yes")
                    #         x.type = pygame.KEYUP
                    #         if x.key == pygame.K_w:
                    #             player.y_change += -player.y_dist
                    #
                    #         elif x.key == pygame.K_s:
                    #             player.y_change += player.y_dist
                    #
                    #         elif x.key == pygame.K_d:
                    #             player.x_change += player.x_dist
                    #
                    #         elif x.key == pygame.K_a:
                    #             player.x_change += -player.x_dist

                    PAUSE = False
                    ENDLESS = True

                if 666 <= pos[0] <= 1088 and 470 <= pos[1] <= 616:  # Home
                    for x in all_sprites_list:
                        x.kill()

                    for x in background_list:
                        x.kill()

                    First_Var = 0

                    PAUSE = False
                    HOME = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:

                    PAUSE = False
                    ENDLESS = True

                if event.key == pygame.K_ESCAPE:
                    PAUSE = False
                    HOME = True

            pygame.display.update()

    if DEATH == True:
        screen.fill(BLACK)

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()

                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    newscore = 0
                    death_score = 0
                    score = 0
                    DEATH = False
                    HOME = True

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()