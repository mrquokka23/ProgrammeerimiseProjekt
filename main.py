import pygame
import math
from pygame.locals import * # import pygame.locals for easier access to key coordinates
from sys import exit
import random

pygame.init()
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()