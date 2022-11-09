import pygame
import math
from pygame.locals import * # import pygame.locals for easier access to key coordinates
from sys import exit
import random
import time

pygame.init()
clock = pygame.time.Clock()
bgimg = pygame.image.load('ProgrammeerimiseProjekt/assets/road.jpg') #loads in the background image
screen_width = bgimg.get_width() 
screen_height = bgimg.get_height()

screen = pygame.display.set_mode((screen_width, screen_height)) #sets the screen size
pygame.display.set_caption("Racer Game") #sets the name of the opened window

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ProgrammeerimiseProjekt/assets/playercar.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, -90)
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width/2, screen_height-100)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # move the sprite based on the key pressed
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(5, 0)

        # keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 640:
            self.rect.right = 640
    
    def draw(self, surface):
        # blit yourself at your current position
        surface.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ProgrammeerimiseProjekt/assets/playercar.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90)
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (320, 240)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # move enemy down the screen
        self.rect.move_ip(0, 1)
        # if image is off screen, kill it
        if self.rect.top > screen_height:
            self.kill()
    
    def draw(self, surface):
        # blit yourself at your current position
        surface.blit(self.image, self.rect)

player = Player() # create player
enemies = [] # create enemy list
enemy_locations = [64, 148, 240, 330, 420] # define enemy spawn locations
def create_enemies():
    for e in range(random.randint(1,5)):
        if not enemies:
            enemies.append(Enemy())
            enemies[0].rect.center = (random.choice(enemy_locations), 0-enemies[0].rect.height/2)
        else:
            enemy = Enemy()
            enemy.rect.center = (random.choice(enemy_locations), 0-enemy.rect.height/2)
            checked = False
            while not checked:
                for i in enemies:
                    if not pygame.sprite.collide_mask(enemy, i):
                        enemies.append(enemy)
                        checked = True
                        break
                if not checked:
                    enemy.rect.center = (random.choice(enemy_locations), 0-enemy.rect.height/2)
                else:
                    break
create_enemies()

font = pygame.font.SysFont("opensans", 50)
enemy_timer = time.perf_counter()
enemy_random_timer = 150
loop_counter = 0
scroll = 0
tiles = math.ceil(screen_height / bgimg.get_height()) + 1 
points = 0
speed = 30

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    screen.fill((0,0,0)) #clear the screen before drawing on it 

    clock.tick(speed) 
    if points % 100 == 0:
        speed += 5

    #scroll background 
    scroll = (scroll + 1) % bgimg.get_height()
    for y in range(tiles):
        screen.blit(bgimg, (0, (y-1) * bgimg.get_height() + scroll))

    # update player position
    player.update()
    # update enemy position
    for e in enemies:
        e.update()
    if loop_counter == enemy_random_timer:
        create_enemies()
        enemy_random_timer = random.randint(150, 400)
        loop_counter = 0

    # check for collisions
    for e in enemies:
        if pygame.sprite.collide_mask(player, e):
            while True:
                screen.blit(font.render("Game Over", 1, (255, 255, 255)), (screen_width/2-100, screen_height/2-100))
                screen.blit(font.render("Points: " + str(points), 1, (255, 255, 255)), (screen_width/2-100, screen_height/2-50))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()

    # draw player
    player.draw(screen)
    # draw enemies
    for e in enemies:
        e.draw(screen)

    text = font.render("Points: " + str(points), True, (0 , 255, 0))
    screen.blit(text, (100, 10))

    pygame.display.update()
    loop_counter += 1
    points += 1