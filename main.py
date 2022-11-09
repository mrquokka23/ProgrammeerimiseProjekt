import pygame
import math
from pygame.locals import * # import pygame.locals for easier access to key coordinates
from sys import exit
import random

pygame.init()
clock = pygame.time.Clock()
bgimg = pygame.image.load('ProgrammeerimiseProjekt/assets/road.jpg') #loads in the background image
screen_width = bgimg.get_width() 
screen_height = bgimg.get_height()

screen = pygame.display.set_mode((screen_width, screen_height)) #sets the screen size
pygame.display.set_caption("Racer Game") #sets the name of the opened window

scroll = 0
tiles = math.ceil(screen_height / bgimg.get_height()) + 1 

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    screen.fill((0,0,0)) #clear the screen before drawing on it 
    clock.tick(30) 
    #scroll background 
    scroll = (scroll + 1) % bgimg.get_height()
    for y in range(tiles):
        screen.blit(bgimg, (0, (y-1) * bgimg.get_height() + scroll))

    pygame.display.update()