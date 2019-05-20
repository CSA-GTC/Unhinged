import pygame, sys, random, math
import pygame as pg
from pygame.locals import *

backgroundc = (0, 0, 0)
entity_color = (255, 255, 255)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
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
    the gamen
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
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("satelite_im.jpg").convert_alpha()

        self.rect = self.image.get_rect()


class Health(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.image.load("heart3.png").convert_alpha()

        self.rect = self.image.get_rect()


class Ammo(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.image.load("ammo.png").convert_alpha()

        self.rect = self.image.get_rect()


class Player(Paddle):
    """The player controlled Paddle"""

    def __init__(self, x, y, width, height, screen_rect):
        super(Player, self).__init__(x, y, width, height)

        # How many pixels the Player Paddle should move on a given frame.
        self.y_change = 0
        self.x_change = 0
        # How many pixels the paddle should move each frame a key is pressed.
        self.x_dist = 8
        self.y_dist = 8

        self.orig_image = pygame.image.load("survivor-gun.png").convert_alpha()  #
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

    def MoveKeyDown(self, key):
        """Responds to a key-down event and moves accordingly"""
        if (key == pygame.K_w):
            if background.rect.y > window_height / 2 - self.width:
                background.rect.y = window_height / 2 - self.width
            else:
                self.y_change += -self.y_dist
        elif (key == pygame.K_s):
            if background.rect.y < - 2325 + window_height / 2 + self.width:
                background.rect.y = - 2325 + window_height / 2 + self.width
            else:
                self.y_change += self.y_dist
        elif (key == pygame.K_d):
            if background.rect.x < - 4134 + window_width / 2 + self.width:
                background.rect.x = - 4134 + window_width / 2 + self.width
            else:
                self.x_change += self.x_dist
        elif (key == pygame.K_a):
            if background.rect.x > window_width / 2 - self.width:
                background.rect.x = window_width / 2 - self.width
            else:
                self.x_change += -self.x_dist

    def MoveKeyUp(self, key):
        """Responds to a key-up event and stops movement accordingly"""
        if (key == pygame.K_w):
            self.y_change += self.y_dist

        elif (key == pygame.K_s):
            self.y_change += -self.y_dist

        elif (key == pygame.K_d):
            self.x_change += -self.x_dist

        elif (key == pygame.K_a):
            self.x_change += self.x_dist

    def EntMoveX(self):
        for en in enemy_list:
            en.rect.move_ip(-self.x_change, 0)

    def EntMoveY(self):
        for en in enemy_list:
            en.rect.move_ip(0, -self.y_change)

    def Borders(self):
        hity = 0
        hitx = 0
        background.rect.move_ip(-self.x_change, -self.y_change)

        if background.rect.y > window_height / 2 - self.width:
            background.rect.y = window_height / 2 - self.width
            hity += 1

        elif background.rect.y < - map_height + window_height / 2 + self.width:
            background.rect.y = - map_height + window_height / 2 + self.width
            hity += 1

        if background.rect.x < - map_width + window_width / 2 + self.width:
            background.rect.x = - map_width + window_width / 2 + self.width
            hitx += 1

        if hity == 0:
            self.EntMoveY()
            for en in heart_list:
                en.rect.move_ip(0, -self.y_change)

            for en in ammo_list:
                en.rect.move_ip(0, -self.y_change)

        if hitx == 0:
            self.EntMoveX()
            for en in heart_list:
                en.rect.move_ip(-self.x_change, 0)

            for en in ammo_list:
                en.rect.move_ip(-self.x_change, 0)

    def update(self):
        """
        Moves the paddle while ensuring it stays in bounds
        """
        self.get_angle()
        self.Borders()


class Enemy(pygame.sprite.Sprite):
    """
    AI controlled paddle, simply moves towards the ball
    and nothing else.
    """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()


        #self.rect = self.image.get_rect()

        num = random.randint(3, 5)
        self.y_change = num
        self.x_change = num

        self.orig_image = pygame.image.load("zombie1.png").convert_alpha()  #
        self.image = self.orig_image
        self.rect = self.image.get_rect(center=screen_rect.center)
        self.angle = 0
        self.distance = 0
        self.angle_offset = 0

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def get_angle(self):
        #mouse = pg.mouse.get_pos()
        offset = (self.rect.centerx - window_width/2, self.rect.centery - window_height/2)
        self.angle = math.degrees(math.atan2(*offset)) - self.angle_offset
        old_center = self.rect.center
        self.image = pg.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect(center=old_center)
        self.distance = math.sqrt((offset[0] * offset[0]) + (offset[1] * offset[1]))


    def update(self):
        """
        Moves the Paddle while ensuring it stays in bounds
        """
        self.get_angle()
        # Moves the Paddle up if the ball is above,
        # and down if below.
        if player.rect.y < self.rect.y:
            self.rect.y -= self.y_change
        elif player.rect.y > self.rect.y:
            self.rect.y += self.y_change

        if player.rect.x < self.rect.x:
            self.rect.x -= self.x_change
        elif player.rect.x > self.rect.x:
            self.rect.x += self.x_change


pygame.init()

window_width = 1500
window_height = 800
map_height = 2325
map_width = 4134
screen = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Dodge the Fire Zombies!!!")

clock = pygame.time.Clock()

screen_rect = screen.get_rect()

player = Player(window_width / 2, window_height / 2, 40, 40, screen_rect)

background = Background()

bullet_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
heart_list = pygame.sprite.Group()
ammo_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(background)
all_sprites_list.add(player)

for x in range(25):
    enemy = Enemy()
    enemy.rect.x = random.randint(background.rect.x, background.rect.x + map_width)
    enemy.rect.y = random.randint(background.rect.x, background.rect.x + map_height)
    all_sprites_list.add(enemy)
    enemy_list.add(enemy)

ammunition = 100
fontObj = pygame.font.Font('freesansbold.ttf', 32)
textSurfaceObj = fontObj.render("AMMO = " + str(ammunition), True, WHITE)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (1100, 50)

lives = 100
fontObj2 = pygame.font.Font('freesansbold.ttf', 32)
textSurfaceObj2 = fontObj2.render("HEALTH = " + str(lives) + "%", True, WHITE)
textRectObj2 = textSurfaceObj2.get_rect()
textRectObj2.center = (window_width / 2, 50)

score = 0
fontObj3 = pygame.font.Font('freesansbold.ttf', 32)
textSurfaceObj3 = fontObj3.render("SCORE = " + str(score), True, WHITE)
textRectObj3 = textSurfaceObj3.get_rect()
textRectObj3.center = (400, 50)

fontObj4 = pygame.font.Font('freesansbold.ttf', 32)
textSurfaceObj4 = fontObj4.render('Dodge the Fire Zombies!', True, RED)
textRectObj4 = textSurfaceObj4.get_rect()
textRectObj4.center = (window_width / 2, 100)

fontObj5 = pygame.font.Font('freesansbold.ttf', 32)
textSurfaceObj5 = fontObj5.render('You Died!', True, RED)
textRectObj5 = textSurfaceObj5.get_rect()
textRectObj5.center = (window_width / 2, 100)

fontObj6 = pygame.font.Font('freesansbold.ttf', 32)
textSurfaceObj6 = fontObj6.render("Press 'SPACE' to continue or 'ESCAPE' to exit", True, WHITE)
textRectObj6 = textSurfaceObj6.get_rect()
textRectObj6.center = (window_width / 2, 500)

fontObj7 = pygame.font.Font('freesansbold.ttf', 32)
textSurfaceObj7 = fontObj7.render("Press 'SPACE' to start game, '1' to learn the rules, "
                                  "or 'ESCAPE' to exit", True, WHITE)
textRectObj7 = textSurfaceObj7.get_rect()
textRectObj7.center = (window_width / 2, 500)

fontObj8 = pygame.font.Font('freesansbold.ttf', 32)
textSurfaceObj8 = fontObj8.render("RULES: The objective is to survive for as long as possible by shooting ", True, WHITE)
textRectObj8 = textSurfaceObj8.get_rect()
textRectObj8.center = (window_width / 2, 300)

fontObj9 = pygame.font.Font('freesansbold.ttf', 32)
textSurfaceObj9 = fontObj8.render("enemies to gain score and obtaining ammo and health consumables.", True, WHITE)
textRectObj9 = textSurfaceObj9.get_rect()
textRectObj9.center = (window_width / 2, 400)

pygame.mixer.music.load('Horde.mp3')
pygame.mixer.music.play(-1, 0.0)


GAME = True

START = True
RULES = False
RUNNING = False
DEATH = False

while GAME:

    if START == True:
        screen.fill(BLACK)
        screen.blit(textSurfaceObj4, textRectObj4)
        screen.blit(textSurfaceObj7, textRectObj7)

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    START = False
                    RUNNING = True

                if event.key == pygame.K_1:
                    START = False
                    RULES = True

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    if RULES == True:
        screen.fill(BLACK)

        screen.blit(textSurfaceObj4, textRectObj4)
        screen.blit(textSurfaceObj8, textRectObj8)
        screen.blit(textSurfaceObj9, textRectObj9)
        screen.blit(textSurfaceObj6, (400, 500))

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    RULES = False
                    START = True

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    if RUNNING == True:
        # Event processing here
        chance = 20
        chance_to_spawn = random.randint(1, chance)

        if chance_to_spawn == 1:
            enemy = Enemy()
            enemy.rect.x = random.randint(background.rect.x, background.rect.x + map_width)
            enemy.rect.y = random.randint(background.rect.x, background.rect.x + map_height)
            all_sprites_list.add(enemy)
            enemy_list.add(enemy)

        chance2 = 200
        chance_to_spawn2 = random.randint(1, chance2)

        if chance_to_spawn2 == 1:
            health = Health()
            health.rect.x = random.randint(background.rect.x, background.rect.x + map_width)
            health.rect.y = random.randint(background.rect.x, background.rect.x + map_height)
            all_sprites_list.add(health)
            heart_list.add(health)

        if chance_to_spawn2 == 2:
            ammo = Ammo()
            ammo.rect.x = random.randint(background.rect.x, background.rect.x + map_width)
            ammo.rect.y = random.randint(background.rect.x, background.rect.x + map_height)
            all_sprites_list.add(ammo)
            ammo_list.add(ammo)


        for event in pygame.event.get():
            mouse_pressed = pygame.mouse.get_pressed()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                player.MoveKeyDown(event.key)

            elif event.type == pygame.KEYUP:
                player.MoveKeyUp(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN and mouse_pressed[0] and ammunition != 0:
                soundObj = pygame.mixer.Sound('Gunfire.wav')
                soundObj.play()
                ammunition -= 1
                fontObj = pygame.font.Font('freesansbold.ttf', 32)
                textSurfaceObj = fontObj.render("AMMO = " + str(ammunition), True, WHITE)
                textRectObj = textSurfaceObj.get_rect()
                textRectObj.center = (1100, 50)
                bullet = Bullet()

                bullet.rect.x = window_width / 2
                bullet.rect.y = window_height / 2

                all_sprites_list.add(bullet)
                bullet_list.add(bullet)

        for bullet in bullet_list:
            block_hit_list = pygame.sprite.spritecollide(bullet, enemy_list, True)

            # For each block hit, remove the bullet and add to the score
            for block in block_hit_list:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)

                score += 10
                fontObj3 = pygame.font.Font('freesansbold.ttf', 32)
                textSurfaceObj3 = fontObj2.render("SCORE = " + str(score), True, WHITE)
                textRectObj3 = textSurfaceObj2.get_rect()
                textRectObj3.center = (400, 50)

        player_hit_list = pygame.sprite.spritecollide(player, heart_list, True)

        for hit in player_hit_list:
            score += 10
            fontObj3 = pygame.font.Font('freesansbold.ttf', 32)
            textSurfaceObj3 = fontObj2.render("SCORE = " + str(score), True, WHITE)
            textRectObj3 = textSurfaceObj2.get_rect()
            textRectObj3.center = (400, 50)

            lives += 25
            if lives > 100:
                lives = 100
            fontObj2 = pygame.font.Font('freesansbold.ttf', 32)
            textSurfaceObj2 = fontObj2.render("HEALTH = " + str(lives) + "%", True, WHITE)
            textRectObj2 = textSurfaceObj2.get_rect()
            textRectObj2.center = (window_width / 2, 50)

            heart_list.remove(hit)
            all_sprites_list.remove(hit)

        player_hit_list = pygame.sprite.spritecollide(player, ammo_list, True)

        for hit in player_hit_list:
            score += 10
            fontObj3 = pygame.font.Font('freesansbold.ttf', 32)
            textSurfaceObj3 = fontObj2.render("SCORE = " + str(score), True, WHITE)
            textRectObj3 = textSurfaceObj2.get_rect()
            textRectObj3.center = (400, 50)

            ammunition += 25
            fontObj = pygame.font.Font('freesansbold.ttf', 32)
            textSurfaceObj = fontObj.render("AMMO = " + str(ammunition), True, WHITE)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (1100, 50)

            ammo_list.remove(hit)
            all_sprites_list.remove(hit)

        for enemy1 in enemy_list:
            for enemy2 in enemy_list:
                if enemy1.rect.colliderect(enemy2.rect):
                    enemy1.rect.x -= 2
                    enemy1.rect.y -= 2
                    enemy2.rect.y += 2
                    enemy2.rect.x += 2

        player_hit_list = pygame.sprite.spritecollide(player, enemy_list, True)

        for hit in player_hit_list:
            lives -= 3
            fontObj2 = pygame.font.Font('freesansbold.ttf', 32)
            textSurfaceObj2 = fontObj2.render("HEALTH = " + str(lives) + "%", True, WHITE)
            textRectObj2 = textSurfaceObj2.get_rect()
            textRectObj2.center = (window_width / 2, 50)
            enemy_list.remove(hit)
            all_sprites_list.remove(hit)

        if lives <= 0:
            for x in all_sprites_list:
                x.kill()

            for x in bullet_list:
                x.kill()

            for x in enemy_list:
                x.kill()

            ammo = 100
            score = 0
            lives = 100

            player = Player(window_width / 2, window_height / 2, 40, 40, screen_rect)
            background = Background()

            all_sprites_list.add(background)
            all_sprites_list.add(player)

            for x in range(25):
                enemy = Enemy()
                enemy.rect.x = random.randint(background.rect.x, background.rect.x + map_width)
                enemy.rect.y = random.randint(background.rect.x, background.rect.x + map_height)
                all_sprites_list.add(enemy)
                enemy_list.add(enemy)

            RUNNING = False
            DEATH = True

        for ent in all_sprites_list:
            ent.update()

        all_sprites_list.draw(screen)
        screen.blit(textSurfaceObj2, textRectObj2)
        screen.blit(textSurfaceObj, textRectObj)
        screen.blit(textSurfaceObj3, textRectObj3)

        pygame.display.update()
        pygame.display.flip()
        screen.fill(backgroundc)

        clock.tick(60)

    if DEATH == True:
        screen.fill(BLACK)

        screen.blit(textSurfaceObj5, textRectObj5)
        screen.blit(textSurfaceObj3, (650, 300))
        screen.blit(textSurfaceObj6, textRectObj6)

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()

                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    score = 0
                    DEATH = False
                    START = True

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()