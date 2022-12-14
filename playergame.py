import os
import pygame
import math
# import pygame.locals for easier access to key coordinates
from pygame.locals import *
from sys import exit
import random
import time
import cv2
from aigame import Player, create_enemies, check_and_remove_enemies

local_dir = os.path.dirname(__file__)


def playergame():
    pygame.init()
    clock = pygame.time.Clock()
    # loads in the background image
    bgimg = pygame.image.load(local_dir + '/assets/road.jpg')
    screen_width = bgimg.get_width()
    screen_height = bgimg.get_height()
    blackplayer = cv2.imread(
        local_dir + "/assets/playercar.png", cv2.IMREAD_UNCHANGED)
    ret, mask = cv2.threshold(blackplayer[:, :, 3], 0, 255, cv2.THRESH_BINARY)
    cv2.imwrite(local_dir + '/assets/black-and-white.png', mask)
    blackplayer = pygame.image.load(local_dir + '/assets/black-and-white.png')
    blackplayer = pygame.transform.rotate(blackplayer, 90)
    blackplayer = pygame.transform.scale(blackplayer, (55, 105))
    blackimg = pygame.image.load(local_dir + '/assets/road.jpg')
    screen = pygame.display.set_mode(
        (screen_width, screen_height))  # sets the screen size
    # sets the name of the opened window
    pygame.display.set_caption("Racer Game")
    player = Player(screen_width=screen_width,
                    screen_height=screen_height)  # create player
    enemies = []  # create enemy list
    enemies = create_enemies()

    font = pygame.font.SysFont("opensans", 50)
    enemy_random_timer = 300
    loop_counter = 0
    scroll = 0
    tiles = math.ceil(screen_height / bgimg.get_height()) + 1
    loops = 0
    speed = 400

    run = True
    while run:
        blackimg.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        screen.fill((0, 0, 0))  # clear the screen before drawing on it

        clock.tick(speed)
        if loops % 100 == 0 and speed < 100:
            speed += 5
        if speed > 100:
            speed = 100

        # scroll background
        scroll = (scroll + 1) % bgimg.get_height()
        for y in range(tiles):
            screen.blit(bgimg, (0, (y-1) * bgimg.get_height() + scroll))

        # update player position
        player.draw(screen)
        # update enemy position

        if loop_counter == enemy_random_timer:
            enemies.extend(create_enemies())
            enemy_random_timer = random.randint(300, 400)
            loop_counter = 0
        check_and_remove_enemies(enemies)

        for e in enemies:
            if e.update(screen_height):
                enemies.remove(e)
            else:
                e.draw(screen)

        # check for collisions
        for e in enemies:
            if pygame.sprite.collide_mask(player, e):
                pygame.display.update()
                player.kill()
                run = False

        text = font.render("Points: " + str(loops), True, (0, 255, 0))
        screen.blit(text, (100, 10))

        pygame.display.update()
        loop_counter += 1
        player.update(gamemode=1, black=blackimg,
                      screen_width=screen_width, screen_height=screen_height)
        player.draw(screen)
        if player.rect.x < 0:
            player.rect.x = 0
        elif player.rect.x + player.rect.width > screen_width:
            player.rect.x = screen_width - player.rect.width

        loops += 1
    back = False
    while not back:
        for event in pygame.event.get():
            if event.type == QUIT:
                back = True
            if event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_ESCAPE:
                    back = True

        screen.fill((255, 255, 255))
        text = font.render("Points: " + str(loops), True, (0, 0, 0))
        gameover = font.render("Game Over", True, (0, 0, 0))
        backtext = font.render("Press space to go", True, (0, 0, 0))
        backtext1 = font.render("back to main menu", True, (0, 0, 0))
        screen.blit(gameover, (screen_width/2-gameover.get_width() /
                    2, screen_height/2-gameover.get_height()/2 - 100))
        screen.blit(text, (screen_width/2-text.get_width() /
                    2, screen_height/2-text.get_height()/2))
        screen.blit(backtext, (screen_width/2-backtext.get_width() /
                    2, screen_height/2-backtext.get_height()/2 + 100))
        screen.blit(backtext1, (screen_width/2-backtext1.get_width() /
                    2, screen_height/2-backtext1.get_height()/2 + 150))
        pygame.display.update()
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            back = True

    return loops
